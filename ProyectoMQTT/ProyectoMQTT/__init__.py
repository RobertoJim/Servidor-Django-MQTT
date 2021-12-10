from . import mqtt
from . import weather



weather.openWeatherMap()  
weather.comprobarMes()
mqtt.client.loop_start()

#aqui deberia de haber una funcion que sincronize los estados toldo y persiana con el esp32, para que cuando visites la interfaz
# despues de que el arduino haya arrancado, estar sincronizado
#puedo hacerlo de la siguiente manera: 
# lo que se me ocurre es que cuando te conectes mandes un topic al esp32, que te responda con otro topic mandandote los estados