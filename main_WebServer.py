#librerías
import network
import socket
from machine import Pin
import time

#----------------------Conexión al punto de acceso------------------------------

#datos de la red a conectarse
essid = 'Edwar_Wifi'
password = 'Electro1'

wlan = network.WLAN(network.STA_IF) #para conectar a una red existente
print('WLAN creada\n')

wlan.active(True)   #activar
print('WLAN activa\n')

wlan.connect(essid, password)
print('Conectandose a la red: %s\n' % essid) #print('Conectandose a: ', essid)

while not wlan.isconnected():   #espera a que se conecte
    print('.')
    time.sleep(1)
    pass

print('Conectado a la red: %s' % essid) #conectado

IP = wlan.ifconfig()
print('IP asignada: %s\n' % IP[0])

#---------------------Creación del servidor web (html)--------------------------

#plantilla de html
template = """<!DOCTYPE html>
              <html>
                <head> <title>Ejemplo de publicacion ESP32</title> </head>
                <body>
                    <h1>Variable:</h1>
                    <table border="1">
                     <input type="text" placeholder= "%s">
                    </table>
                </body>
              </html>"""

s = socket.socket()     #declara socket para publicar el html
s.bind( (wlan.ifconfig()[0],80) )       #IP previamente definida
s.listen(5)
print('Socket creado')
print('esperando acceso desde el navegador\n')

while True:         #ciclo de publicación de la página web

    conn, addr = s.accept()     #cuando se solicite acceso externo
    print('Acceso desde la IP: %s\n' % addr[0])

    conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    print('envio de la cadena de configuracion\n')
    
    variable = str(10000)    
    #variable = '%s'  #variable 
   
    html = template % '\n'.join(variable)   #agrega las nuevas filas a la tabla
    print('Completa la tabla en la plantilla')

    conn.sendall(html)      #env閾哸 el html
    print('Publicacion del HTML\n')

    conn.close()    #cierra la comunicación


