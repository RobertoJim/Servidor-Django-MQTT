from pymodbus.client import ModbusTcpClient
from pymodbus.transaction import ModbusRtuFramer as ModbusFramer
import threading
import time
from datetime import datetime
import pytz
import mysql.connector as mysql_db

arrayPotencia = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
arrayHoraPotencia = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']

def getData():
    global arrayPotencia
    global arrayHoraPotencia
    client = ModbusTcpClient('192.168.1.128', port=502, framer=ModbusFramer)
    client.connect()
    time.sleep(5)
    while(1):
        try:
            data = client.read_input_registers(address=88, count=2, slave = 1)
            potenciaActiva = (data.registers[0] << 16) + data.registers[1]
            print(potenciaActiva)
            T_Datos = "Power_table"
            T_Columnas = "(Fecha, Potencia)"
            T_Valores = f"CURRENT_TIMESTAMP, {potenciaActiva}"
            mainquery = "INSERT INTO"

            __conn = mysql_db.connect(host="192.168.1.100",user="root",passwd="monsol",db="domo")
            SQL_Query = mainquery + " " + T_Datos + " " + T_Columnas + " VALUES (" + T_Valores + ")"
            #print(SQL_Query)
            cursor = __conn.cursor()
            cursor.execute(SQL_Query)

            __conn.commit()
            time.sleep(1)
       	    __conn.close()		
            arrayPotencia.pop(0) # Similar a shift en javascript 
            arrayPotencia.append(str(potenciaActiva)) # Similar a push en javascript
            arrayHoraPotencia.pop(0) # Similar a shift en javascript
            print(arrayPotencia) 
            arrayHoraPotencia.append((str(datetime.now(pytz.timezone('Europe/Madrid')).hour) + ":" + str(datetime.now().minute) + ":" + str(datetime.now().second)))
            time.sleep(60)
        except Exception as e:
            print(e)

def startLoop():
    thread = threading.Thread(target=getData, daemon=True) #Hilo demonio para que se elimine al finalizar el programa
    thread.start()



if __name__ == "__main__":
    getData()
