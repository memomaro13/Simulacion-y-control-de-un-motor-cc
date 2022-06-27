# Control de un motor de corriente directa, variando su voltaje por mqtt
# Por: Francisco Alejandro Alaffita Hernández
# Fecha: 8 de junio de 2022
#
# Materiales necesarios
# 1. Archivo read_RPM.py
# 2. Puente H, L298N
# 3. Motor de corriente directa de 12v con encoder
# 4. Fuente de 12 v
#
# Este programa recibe un valor de 0 a 100% por mqtt, el cual representa el porcentaje
# del voltaje total suministrado al motor por medio del shield L298N.
# Este programa envía el voltaje solicitado al L298N y el motor de corriente directa
# comienza a girar, el programa comienza a medir las RPM por medio del encoder que viene
# integrado con el motor y envía éstas RPM's por medio de mqtt.
#
# Se espera acoplar este programa con Node-Red, el cual tendrá el control del motor por medio
# de los porcentajes de voltaje suministrados, todo el control es a través de mqtt
#
# Raspberry     L298N
#     23  -------In2
#     24  -------In1
#     25  -------en
#     GND -------GND
#
# Librerias para la pantalla Oled
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106
import socket
from PIL import ImageFont, ImageDraw, Image

#Para la pantalla
serial = i2c(port=1, address=0x3c)
#device = ssd1306(serial, rotate=0)
device = sh1106(serial, width=128, height=64, rotate=0)
#device.capabilities(width=128, height=64, rotate=0)
print("size: " , device.bounding_box)
device.clear()

# Librerias para MQTT
import paho.mqtt.client as mqtt # Importa la libreria MQTT 

#Librerias para los pines de entrada
import RPi.GPIO as GPIO
from time import sleep
import pigpio

# Libreria para cosas de mate
import numpy as np
from sklearn import linear_model
# Libreria para obtener las RPM's
from read_RPM import reader # Archivo read_RPM contiene a la clase reader
Vin=0
def messageFunction (client, userdata, message):
    global x
    global Vin
    topic = str(message.topic)
    message = int(message.payload.decode("utf-8")) # transformamos el mensaje de texto a entero
    if message>=0 and message <=100:
        #print(message)
        Vin=12*message/100
        p.ChangeDutyCycle(message) # Aquí ocurre la magia para el cambio de voltaje
    elif message==-1:
        x=-1
    elif message==-2:
        x=-2
    else:
        print('El porcentaje debe estar entre 0 y 100')
        
broker_address="18.157.172.72" # IP de hivemq, se puede poner 'hivemq.com' pero tarda un poco
ourClient = mqtt.Client("Alex_Alaffita") # Crea un objeto para el cliente de mqtt
ourClient.connect(broker_address, 1883) # Este nos conecta al broker, también funciona con la
                                    # url es decir "hivemq.com"
ourClient.subscribe("capstone/salon/virtual") # El topic para suscribirnos
ourClient.on_message = messageFunction # Para pegar el mensaje dentro de la variable
ourClient.loop_start() # Para comenzar el cliente de mqtt

# Pines de conexión con el shield L298N
in1 = 24 
in2 = 23
en = 25


GPIO.setmode(GPIO.BCM) # Para fijar el modo para los pines

GPIO.setup(in1,GPIO.OUT) # Definimos a in1 como de salida en raspberry
GPIO.setup(in2,GPIO.OUT) # Definimos a in2 como de salida en raspberry
GPIO.setup(en,GPIO.OUT)  # Definimos a en como de salida en raspberry
GPIO.output(in1,GPIO.LOW)# Para estar seguros que el motor se detiene antes de comenzar 
GPIO.output(in2,GPIO.LOW)# Para estar seguros que el motor se detiene antes de comenzar
p=GPIO.PWM(en,2000) # La frecuencia para el pulso PWM en el pin en, de la variable p
p.start(25) # Para comenzar con el 25% con el movimiento del motor
print("\n")
print("Recuerda que debes de suministrar un porcentaje del voltaje (entre 0 y 100)")
print("Esperando...")
print("\n")    

cont=0  #Contador de pulsos
 
# Set up RPM reader
RPM_GPIO = 6 # PIN GPIO de entrada en Raspberry
SAMPLE_TIME = 0.1 # Tiempo de muestreo para medir la velocidad

pi = pigpio.pi() # Creación de la variable pi
pi.set_servo_pulsewidth(RPM_GPIO, 2500) # Maximum throttle.
sleep(2)
pi.set_servo_pulsewidth(RPM_GPIO, 500) # Minimum throttle.
sleep(2)
ppc=334 # Pulsos por ciclo, el encoder tiene 334 marcas en la rueda
tach = reader(pi, RPM_GPIO,ppc) # Función de lectura del encoder, se especifica la variable
                                # El pin en donde se encuentra y los pulsos por ciclo

#Iniciamos el motor de dc con el 0% del voltaje total (12 v) 
 
GPIO.output(in1,GPIO.HIGH)
GPIO.output(in2,GPIO.LOW)
p.ChangeDutyCycle(0)
x=1

# Cálculo  de la simulación
t=0;
b=7.10639123732791
caux=81088.9809185961
A=np.array([[1,1],[0,-b]])
k1=0;
k2=0;
while(x==1 or x==-2):
        
    rpm = tach.RPM() # Función para leer las rpm
    #print(rpm)
    ourClient.subscribe("capstone/salon/virtual/voltaje") # Subscribe message to MQTT broker
    ourClient.publish("capstone/salon/virtual/RPM",str(rpm)) # Publish message to MQTT broker    
    if x==-2:
        i=0
        p.ChangeDutyCycle(100) # Ponemos a velocidad máxima al motor
        w=np.zeros(200) # Creamos el vector w con 200 elementos de sólo ceros 
        w2=np.zeros(198) # Igual que en w
        
        # Esta sección es para tomar las 200 muestras de velocidad
        while i<200:
            w[i]=tach.RPM() # Aqui llenamos el vector w con las velocidades
            if i>0 and i<199:
                w2[i-1]=w[i] # Hacemos una copia de w pero sin el primer y el último término
            i=i+1
            sleep(0.01) # Tiempo de muestreo entre cada toma de velocidad
        i=1 # Reiniciamos el contador i
        dw=np.zeros(198) # Creamos ell vector dw (velocidad de w)
        
        # El siguiente fragmento de código calcula la derivada central numérica para w
        while i<199:
            dw[i-1]=(w[i+1]-w[i-1])/0.02 # Diferencias centrales
            i=i+1
        p.ChangeDutyCycle(0) # Apaga el motor después de dos segundos a funcionamiento máximo
    # Creo un modelo de regresión lineal
        modelo = linear_model.LinearRegression()
    # Entreno el modelo con los datos (X,Y)
        modelo.fit(w2.reshape(-1,1), dw)
        print(modelo.coef_[0])
        print(modelo.intercept_)
        x=1       
        b=-modelo.coef_[0]
        A=np.array([[1,1],[0,-b]])
        print(A)
        caux=modelo.intercept_
    # Cálculo de los coeficientes para la ecuación diferencial
    c=(caux)*Vin/12
    B=np.array([[k1],[k2-c/b]])
    invA=np.linalg.inv(A) # Inversa de la matriz A
    CC=np.dot(invA,B) # Producto de matrices (A^-1)B
# Recuerda que los indices comienzan en 0, así que CC[1] es CC[2]
# en matlab

    dy=(c/b)-b*CC[1]*np.exp(-b*t) # Solución de la ecuación diferencial con todas las constantes
    
    t=t+0.1;
    # Publicación con MQTT de la solución a la ecuación diferencial.
    ourClient.publish("capstone/salon/virtual/RPMsim",str(dy[0]))
    #print(dy)
    sleep(SAMPLE_TIME) # Tiempo de espera entre cada lectura
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
    #font = ImageFont.load_default(size=12)
    #font = ImageFont.truetype(, size=12)
        draw.text((30, 20), "Código IoT", fill="white",size=23)
        draw.text((10, 30),str(rpm), fill="white",fontsize=19)

print("Fin del programa, ¡¡¡Saludos!!!")
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.cleanup() # Limpiamos todos los pines
