#Логика проекта MCBot
#Импорт библиотек
import time
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
#Функция определения моба из майнкрафта
def get_class(path):
    np.set_printoptions(suppress=True)
    model = load_model("keras_model.h5", compile=False)
    class_names = open("labels.txt", "r").readlines()
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open(path).convert("RGB")
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]
    print("Class:", class_name[2:-1], end="")
    print("Confidence Score:", confidence_score)
    return class_name[2:-1]
#Время Самары
def localtime():
    seconds = time.time() + 202
    local_time = time.ctime(seconds)
    return local_time
localtime()
#Время Москвы
def loctime():
    seconds = time.time() + 202 - 3600
    locatime = time.ctime(seconds)
    return locatime
loctime()
