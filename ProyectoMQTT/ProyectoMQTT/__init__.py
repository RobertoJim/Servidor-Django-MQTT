from . import mqtt
from . import weather

weather.openWeatherMap()  
mqtt.iniciarEstados()
mqtt.client.loop_start()

