import streamlit as st
from sentinelhub import (
    SHConfig,
    CRS,
    BBox,
    DataCollection,
    MimeType,
    SentinelHubRequest,
    bbox_to_dimensions,
)
from def_load_image import load_image
from PIL import Image, ImageEnhance

# Установка конфигурации
config = SHConfig()
config.sh_client_id = '57cc91cd-6e3b-4a34-be7c-04516446d800'
config.sh_client_secret = '736oAZLltjnCM95OWxql4CfZ7M25jC4k'


# Главная часть Streamlit-приложения
def main():
    # Установка широкого режима по умолчанию
    st.set_page_config(layout="wide")
    
    st.title("Cпутниковые снимки")

    with st.sidebar:
        
        st.header('Панель управления')

        # Ввод координат области
        latitude = st.number_input("Введите широту", value=120.0)
        longitude = st.number_input("Введите долготу", value=30.0)
        
        # Выбор даты
        date = st.date_input("Выберите дату", value= None)
        
        # Изменение яркости
        brightness = st.slider("Яркость", min_value=0.0, max_value=9.0, value=3.0, step=1.0)
        # Изменение контрастности
        contrast = st.slider("Контрастность", min_value=0.0, max_value=9.0, value=3.0, step=1.0)

    col1,col2 = st.columns([1,1])
    
    #Допустимые значения для широты и долготы (определены подбором)
    trig = True
    if (latitude < -120) or (latitude > 130) :
        trig = False
        st.sidebar.text("Недопустимое значение широты")
    elif (longitude < -35) or (longitude > 75):
        trig = False 
        st.sidebar.text("Недопустимое значение долгготы")   

    if st.sidebar.button("Загрузить спутниковый снимок") and trig :
        try:
            # Загрузка спутникового снимка
            load_image(latitude, longitude, date)
            img = Image.open("path/saved_image.tif")

            # Отображение исходного изображения
            col1.image(img, caption='Исходное изображение', use_column_width=True)

            #Обработка исходного изображение
            mod_image = ImageEnhance.Brightness(img).enhance(brightness)
            mod_image = ImageEnhance.Contrast(mod_image).enhance(contrast)

            # Отображение измененного изображения
            col2.image(mod_image, caption="Обработанное изображение", use_column_width=True)
        except Exception as e:
            st.error(f"Ошибка загрузки спутникового снимка: {e}")
    else:
        text_info = """Данное веб-приложение разработано на базе Streamlit, которое позволит пользователю визуализировать спутниковые снимки 
заданной области и применять к ним базовые операции обработки изображений с использованием Sentinel Hub.
Sentinel Hub - это сервис облачных вычислений и API для работы с геопространственными данными, предоставляющий доступ к 
спутниковым снимкам различных спутников, таких как Sentinel-1, Sentinel-2, Landsat и других."""
        st.text(text_info)
        st.text("Как загрузить изображение")
        st.text("1. Укажите желаемую широту")
        st.text("2. Укажите желаемую долготу")
        st.text("3. Можете выбрать желаемую дату")
        st.text("4. Можете изменить яркость и контрастность")
        st.text('5. Нажмите кнопку "Загрузить спутниковый снимок"')

if __name__ == "__main__":
    main()
