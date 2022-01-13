from . import mqtt
from . import weather
from datetime import datetime
import pytz

weather.openWeatherMap()  
mqtt.iniciarEstados()
mqtt.client.loop_start()

print("La hora es " + str(datetime.now(pytz.timezone('Europe/Madrid')).hour))