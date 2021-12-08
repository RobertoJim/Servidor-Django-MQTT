from . import mqtt
from . import weather



weather.openWeatherMap()  
weather.comprobarMes()
mqtt.client.loop_start()
