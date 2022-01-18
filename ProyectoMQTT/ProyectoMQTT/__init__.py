from . import mqtt
from . import weather
from datetime import datetime


weather.openWeatherMap()  
mqtt.iniciarEstados()
mqtt.client.loop_start()
