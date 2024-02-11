from sentinelhub import SHConfig, BBox, SentinelHubRequest, CRS, MimeType, DataCollection
import imageio
from datetime import datetime

# Установка конфигурации
config = SHConfig()
config.sh_client_id = '57cc91cd-6e3b-4a34-be7c-04516446d800'
config.sh_client_secret = '736oAZLltjnCM95OWxql4CfZ7M25jC4k'

#Функция для загрузки изображения с сервиса Sentinel Hub
def load_image(latitude, longitude,date):
    # Координаты и размеры области 
    bbox = BBox((latitude, longitude, latitude+1, longitude+1), crs=CRS.WGS84)

    if date:
        date = date.strftime("%Y-%m-%d")
    else:
        #Базовое значение, если пользователь не указал дату
        date = "2022-04-22"

    time = datetime.now()
    date_n = time.strftime("%Y-%m-%d")
    # Создание запроса для получения изображения в формате TIFF
    request = SentinelHubRequest(
        evalscript="""
            //VERSION=3

            function setup() {
                return {
                    input: [{
                        bands: ["B02", "B03", "B04"]
                    }],
                    output: {
                        bands: 3
                    }
                };
            }

            function evaluatePixel(sample) {
                return [sample.B04, sample.B03, sample.B02];
            }
        """,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L2A,
                time_interval=(date,date_n),
                #Выбор изображений с облачностью менее 10%
                maxcc=0.1
            )
        ],
        responses=[
            SentinelHubRequest.output_response('default', MimeType.TIFF)
        ],
        bbox=bbox,
        size=(600, 600),
        config=config
    )

    # Загрузка изображения
    image = request.get_data()[0]
    save_path = 'path/saved_image.tif'
    imageio.imwrite(save_path, image)

