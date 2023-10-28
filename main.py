import discord
from discord.ext import commands
import disnake
import asyncio
import re
import datetime
import random
import time
import os
import sqlite3
import yt_dlp as youtube_dl
import ffmpeg
import speech_recognition as sr
import pyttsx3
from main_logic import *
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='&', intents=intents)
db_path = ".\pon.db"
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def пр(ctx):
    await ctx.send(f'**Привет! Я {bot.user}!**')

@bot.command()
async def хах(ctx, count_heh = 5):
    if count_heh > 10:
        await ctx.send("**Максимум 10!**")
    else:
        await ctx.send("**А**" + "**ха**" * count_heh)

@bot.command()
@commands.has_permissions(administrator=True) # though imo i would put just ban_members perm for this.
async def бан(ctx, member: discord.Member, *, reason=None):
    if member == ctx.author:
       await ctx.send("**Ты не можешь забанить себя!**")
       return
    await member.ban(reason=reason)
    await ctx.send("**Пользователь забанен**")
@bot.command()
@commands.has_permissions(ban_members=True, administrator=True)
async def разбан(ctx, member: int, *, reason=None):
    try:
        banned_user = await ctx.guild.fetch_ban(disnake.Object(member))
    except disnake.NotFound:
        await ctx.send(f'**Пользователь с ID {member} не забанен на сервере**', delete_after=10)
        return
    user = banned_user.user
    embed = disnake.Embed(
        title=f"**Вы были разбанены на сервере {ctx.guild.name}**",
        description=f'**Вас разбанил администратор {ctx.author} по причине: "{reason}"**',
        color=0x3aed24
    )
    try:
        await user.send(embed=embed)
    except:
        print(f"**Невозможно отправить табличку пользователю {user}, пропуск**")
        pass
    try:
        await ctx.guild.unban(user, reason=reason)
        await ctx.send(f'**Администратор {ctx.author.mention} разбанил пользователя {user.mention} по причине: "{reason}"**', delete_after=10)
    except:
        await ctx.send(f'**Не удалось разбанить пользователя {user.mention}**', delete_after=10)
    await ctx.message.delete()

@bot.command()
@commands.has_permissions(administrator = True)
async def таймбан(ctx, member: discord.Member, time, *, reason):
    await ctx.send(f'**{member.mention} забанен \n Продолжительность бана: {time}h \n Причина бана: {reason}**')
    await member.send(f'**Тебя забанили на сервере {ctx.guild.name} по причине {reason}**')
    await member.ban(reason=reason)
    def str_time_to_seconds(str_time, language='ru'):
        conv_dict = {
            'w': 'weeks',
            'week': 'weeks',
            'weeks': 'weeks',
            'н': 'weeks',
            'нед': 'weeks',
            'неделя': 'weeks',
            'недели': 'weeks',
            'недель': 'weeks',
            'неделю': 'weeks',

            'd': 'days',
            'day': 'days',
            'days': 'days',
            'д': 'days',
            'день': 'days',
            'дня': 'days',
            'дней': 'days',

            'h': 'hours',
            'h': 'hours',
            'hour': 'hours',
            'hours': 'hours',
            'ч': 'hours',
            'час': 'hours',
            'часа': 'hours',
            'часов': 'hours',

            'm': 'minutes',
            'min': 'minutes',
            'mins': 'minutes',
            'minute': 'minutes',
            'minutes': 'minutes',
            'мин': 'minutes',
            'минута': 'minutes',
            'минуту': 'minutes',
            'минуты': 'minutes',
            'минут': 'minutes',

            's': 'seconds',
            'sec': 'seconds',
            'secs': 'seconds',
            'second': 'seconds',
            'seconds': 'seconds',
            'сек': 'seconds',
            'секунда': 'seconds',
            'секунду': 'seconds',
            'секунды': 'seconds',
            'секунд': 'seconds'
        }
        pat = r'[0-9]+[w|week|weeks|н|нед|неделя|недели|недель|неделю|d|day|days|д|день|дня|дней|h|hour|hours|ч|час|часа|часов|min|mins|minute|minutes|мин|минута|минуту|минуты|минут|s|sec|secs|second|seconds|c|сек|секунда|секунду|секунды|секунд]{1}'
        def timestr_to_dict(tstr):
            #convert 1d2h3m4s to {"d": 1, "h": 2, "m": 3, "s": 4}
            return {conv_dict[p[-1]]: int(p[:-1]) for p in re.findall(pat, str_time)}
        def timestr_to_seconds(tstr):
            return datetime.timedelta(**timestr_to_dict(tstr)).total_seconds()
        def plural(n, arg):
            days = []
            if language == "ru":
                if arg == 'weeks':
                    days = ['неделя', 'недели', 'недель']
                elif arg == 'days':
                    days = ['день', 'дня', 'дней']
                elif arg == 'hours':
                    days = ['час', 'часа', 'часов']
                elif arg == 'minutes':
                    days = ['минута', 'минуты', 'минут']
                elif arg == 'seconds':
                    days = ['секунда', 'секунды', 'секунд']
            elif language == "en":
                if arg == 'weeks':
                    days = ['week', 'weeks', 'weeks']        
                elif arg == 'days':
                    days = ['day', 'day', 'days']
                elif arg == 'hours':
                    days = ['hour', 'hour', 'hours']
                elif arg == 'minutes':
                    days = ['minute', 'minute', 'minutes']
                elif arg == 'seconds':
                    days = ['second', 'second', 'seconds']
            if n % 10 == 1 and n % 100 != 11:
                p = 0
            elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
                p = 1
            else:
                p = 2
            return str(n) + ' ' + days[p]
        counter_in_str = ""
        for i in timestr_to_dict(str_time).items():
            counter_in_str += f"{plural(i[1], i[0])} "
        return int(timestr_to_seconds(str_time)), counter_in_str
    seconds, str_time = str_time_to_seconds(time)
    await asyncio.sleep(seconds)
    await member.unban()
    await ctx.send(f'**У {member.mention} закончился бан**')
    link = await ctx.channel.create_invite(max_age=300)
    await member.send(f'**У тебя закончился бан на сервере "{ctx.guild.name}"! {link}**')

@bot.command()
async def таб(ctx, name: str, *, bio: str):
    if len(bio) > 200:
        await ctx.send("**Слишком длинный рассказ!**")
    else:
        embed = discord.Embed(title=name, colour=0x1900BA, description=bio)
        await ctx.channel.send(embed=embed)

@bot.command()
async def монетка(ctx, moneyy: str):
    if moneyy == "решка":
        ran = random.randint(1, 2)
        time.sleep(1)
        if ran == 1:
            await ctx.send("**Решка, вы выиграли!**")
        if ran == 2:
            await ctx.send("**Орёл, вы проиграли!**")
    if moneyy == "орёл" or moneyy == "орел":
        ra = random.randint(1, 2)
        time.sleep(1)
        if ra == 1:
            await ctx.send("**Орёл, вы выиграли!**")
        if ra == 2:
            await ctx.send("**Решка, вы проиграли!**")

@bot.command()
async def время(ctx, tim="самара"):
    tim = tim.capitalize()
    if tim == "Самара":
        await ctx.send('**Самарское время: 'f'{localtime()}**')
    if tim == "Москва" or tim == "Чебоксары":
        await ctx.send('**Московское время: 'f'{loctime()}**')

@bot.command()
async def счет(ctx, num0: float, znak: str, num1: float):
    if znak == "+":
        await ctx.send(f'{num0 + num1}')
    elif znak == "-":
        await ctx.send(f'{num0 - num1}')
    elif znak == "*":
        await ctx.send(f'{num0 * num1}')
    elif znak == ":" or znak == "/":
        await ctx.send(f'{num0 / num1}')
    elif znak == "**":
        await ctx.send(f'{num0 ** num1}')
    elif znak == "::" or znak == "//":
        await ctx.send(f'{num0 // num1}')
    elif znak == "%":
        await ctx.send(f'{num0 % num1}')
    else:
        await ctx.send("**Всмысле? Либо такого знака нет, либо ты ошибся!**")

@bot.command()
@commands.has_permissions(administrator=True) 
async def кик(ctx, member: discord.Member, *, reason=None):
    if member == ctx.author:
       await ctx.send("**Ты не можешь выгнать себя!**")
       return
    await member.kick(reason=reason)
    await ctx.send(f'**{member} был выгнан с сервера по причине {reason}!**')

@bot.command()
async def геймер(ctx):
    author = ctx.message.author
    guild = bot.get_guild(970323341355417740)
    role = guild.get_role(970337939513020426)
    await author.add_roles(role)
    await ctx.send("**Теперь вы обладаете правами игрока на сервере!**")

@bot.command()
async def моб(ctx):
    try:
        if ctx.message.attachments:
            for attachment in ctx.message.attachments:
                file_name = attachment.filename
                file_url = attachment.url
                await attachment.save(f'images/{file_name}')
                await ctx.send(f'**На картинке: {get_class(f"images/{file_name}")}**')
                await ctx.send(f'**Путь до картинки: {file_url}!**')
                os.remove(f'images/{file_name}')
    except:
        await ctx.send("**Что-то не так**")

@bot.command()
async def таймер(ctx, seconds: int):
    await ctx.send(f"**Таймер запущен на {seconds} секунд.**")
    time.sleep(seconds)
    await ctx.send(f"**Таймер на {seconds} секунд истек!**")
@bot.command()
async def рег(ctx, username: str, age: int, pol: str, *, bio: str):
    if len(bio) > 100:
        await ctx.send("**Слишком длинное описание!**")
    else:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, age INTEGER, pol TEXT, bio TEXT)")
        cursor.execute("INSERT INTO users (username, age, pol, bio) VALUES (?, ?, ?, ?)", (username, age, pol, bio))
        conn.commit()
        conn.close()
        await ctx.send(f'**Пользователь {username} зарегистрирован с возрастом {age} и полом {pol}. Его описание: {bio}**')

@bot.command()
async def инфа(ctx, username: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    conn.close()
    if result:
        username, age, pol, bio = result
        await ctx.send(f'**Имя пользователя: {username}, Возраст: {age}, Пол: {pol}, Описание: {bio}**')
    else:
        await ctx.send(f'**Пользователь {username} не найден.**')

@bot.command()
async def чист(ctx, amount: int):
    await ctx.channel.purge(limit=amount+1)
    await ctx.send(f'**{amount} сообщений было удалено.**')

@bot.command()
async def плэй(ctx, *, query):
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        await ctx.send("Вы должны находиться в голосовом канале, чтобы использовать эту команду.")
        return

    voice_channel = ctx.author.voice.channel
    voice_client = await voice_channel.connect()

    ydl_opts = {
        'outtmpl': 'audio',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        url = info['formats'][0]['url']
        ydl.download([query])
        voice_client.play(discord.FFmpegPCMAudio('audio.mp3'))

    await ctx.send(f'Сейчас играет: {info["title"]}')

@bot.command()
async def цикл(ctx, count: int):
    if ctx.voice_client is None:
        await ctx.send("Я не нахожусь в голосовом канале.")
        return

    if count <= 0:
        await ctx.send("Количество повторений должно быть положительным числом.")
        return

    voice_client = ctx.voice_client

    for _ in range(count):
        voice_client.play(discord.FFmpegPCMAudio('audio.mp3'))
        await discord.utils.sleep_until(lambda: not voice_client.is_playing())

@bot.command()
async def лив(ctx):
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()
        await ctx.send("Я покидаю голосовой канал.")

@bot.command()
async def скип(ctx):
    if ctx.voice_client is None:
        await ctx.send("Не нахожусь в голосовом канале.")
        return

    if not ctx.voice_client.is_playing():
        await ctx.send("Сейчас ничего не играет.")
        return

    ctx.voice_client.stop()
    await ctx.send("Музыка пропущена.")

@bot.command()
async def совет(ctx):
    advice = [
        "Сократите потребление энергии, выключая свет и электроприборы, когда они не используются.",
        "Используйте общественный транспорт или делитесь поездками, чтобы уменьшить выбросы автомобилей.",
        "Переходите на возобновляемые источники энергии, такие как солнечная или ветровая энергия.",
        "Уменьшите использование пластиковых изделий и переходите на альтернативы, такие как стекло или металл.",
        "Практикуйте утилизацию и переработку отходов, чтобы сократить количество мусора, попадающего на свалки.",
        "Поддерживайте местные фермерские рынки и выбирайте продукты, выращенные без использования пестицидов.",
        "Сажайте деревья и растения, чтобы увеличить зеленые зоны и поглотить углекислый газ.",
        "Избегайте использования одноразовых предметов, таких как пластиковые стаканчики и пакеты.",
        "Образуйте сообщества и присоединяйтесь к организациям, которые занимаются проблемами окружающей среды."
    ]
    await ctx.send(f'Вот несколько советов по экологически ответственному поведению:\n\n{random.choice(advice)}')

@bot.command()
async def мотив(ctx):
    motivational_messages = [
    "Не бойтесь делать маленькие шаги - они могут привести к большим изменениям!",
    "Каждое действие имеет значение. Даже маленький вклад может сделать разницу.",
    "Вы можете быть источником вдохновения для других. Делайте то, что вам кажется правильным.",
    "Помните, что каждый шаг в направлении экологически чистой жизни важен. Не недооценивайте свою силу.",
    "Маленькие изменения в повседневной жизни могут привести к большим изменениям для нашей планеты.",
    "Ваш вклад в создание экологически чистого мира может вдохновить других на действие.",
    "Не забывайте, что каждый шаг в направлении более экологически чистой жизни - это шаг в правильном направлении.",
    "Никогда не сомневайтесь в силе своих действий. Ваши маленькие шаги могут привести к большим изменениям."
    ]
    message = random.choice(motivational_messages)
    await ctx.send(message)

@bot.command()
async def ресурсы(ctx):
    resources = [
        "Статья: Как бороться с глобальным потеплением - [тык](https://dzen.ru/a/Wr5yTi9XjAGzWtC_)",
        "Организация: Greenpeace - [тык](https://www.greenpeace.org/)",
        "Руководство: 10 способов снизить углеродный след - [тык](https://ru.wikihow.com/уменьшить-свой-углеродный-след-в-атмосфере)"
    ]
    await ctx.send(f'Вот несколько полезных ресурсов, которые помогут вам узнать больше о глобальном потеплении и способах борьбы с ним:\n\n{resources}')

@bot.command()
async def войс(ctx, *, text):
    if len(text) <= 500:
        engine = pyttsx3.init()
        engine.save_to_file(text, 'voice_message.mp3')
        engine.runAndWait()
        await ctx.send(file=discord.File('voice_message.mp3'))
    else:
        await ctx.send("Ваш текст слишком большой!")

@bot.command()
async def хелп(ctx):
    aboba = ("**&пр - команда приветствия, использование &пр**""\n"
            "**&хах - прикольная команда, использование &хах (кол-во 'ха')**""\n"
            "**&бан - бан пользователя, использование &бан (@пользователь) (причина)**""\n"
            "**&разбан - разбан, использование &разбан (айди пользователя а не @) (причина)**""\n"
            "**&таймбан - временный бан, использование &таймбан (@пользователь) (время например 1s) (причина)**""\n"
            "**&таб - табличка в дс, использование &таб (заголовок) (текст ограниченный в 20 символов)**""\n"
            "**&монетка - монетка, использование &монетка (орёл или решка)**""\n"
            "**&время - время, использование &время (город например москва)**""\n"
            "**&счет - калькулятор, использование &счет (первая цифра или дробь) (знак) (вторая цифра или дробь)**""\n"
            "**&кик - кикает пользователя с сервера, использование &кик (@пользователь) (причина)**""\n"
            "**&геймер - выдача роли игрок, использование &геймер**""\n"
            "**&моб - классификация осовных 4 мобов из майна, использование &моб (прикреплённая картинка)**""\n"
            "**&таймер - таймер на секунды использование &таймер 5**""\n"
            "**&рег - регистрация в базе данных, использование &рег (Имя или @) (возраст в цифрах) (пол) (описание не больше 100 символов)**""\n"
            "**&инфа - инфа о пользователе из базы данных, использование &инфа (@пользователь или имя)**""\n"
            "**&чист - очистка чата, использование &чист (кол-во сообщений для удаления)**""\n"
            "**&плэй - команда для проигрывания музыки из ютуба, использование только если ты в голосовом канале &плэй (ссылка из ютуба)**""\n"
            "**&лив - выход бота из голосового канала, использование только если бот в нём был &лив**""\n"
            "**&цикл - команда, повторяющая последнюю включенную песню, использование &цикл (кол-во повторений в цифрах)**""\n"
            "**&скип - пропуск музыки если она играет, использование &скип**""\n"
            "**&совет - совет по экологии, использование &совет**""\n"
            "**&мотив - мотивация защищать экологию, использование &мотив**""\n"
            "**&ресурсы - разнообразные ресурсы которые иногда могут вам помочь защищать экологию, использование &ресурсы**""\n"
            "**&войс - озвучка голосом бота, использование &войс (текст для озвучки ограниченный в 500 символов)**""\n"
            "**&хелп - помощь по командам, использование &хелп**"
            )
    await ctx.send(aboba)
bot.run("")
