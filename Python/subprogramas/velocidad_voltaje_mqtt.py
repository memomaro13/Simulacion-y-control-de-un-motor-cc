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


import paho.mqtt.client as mqtt # Importa la libreria MQTT 
import RPi.GPIO as GPIO          
from time import sleep
import pigpio
from read_RPM import reader # Archivo read_RPM contiene a la clase reader
# Definición de la clase para la lectura de los mensages de mqtt
def messageFunction (client, userdata, message):
    global x
    topic = str(message.topic)
    message = int(message.payload.decode("utf-8")) # transformamos el mensaje de texto a entero
    if message>=0 and message <=100:
        print(message)
        p.ChangeDutyCycle(message) # Aquí ocurre la magia para el cambio de voltaje
    elif message==-1:
        x=-1
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
p=GPIO.PWM(en,1000) # La frecuencia para el pulso PWM en el pin en, de la variable p
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
while(x==1):
        
    rpm = tach.RPM() # Función para leer las rpm
    print(rpm)
    ourClient.subscribe("capstone/salon/virtual/voltaje") # Subscribe message to MQTT broker
    ourClient.publish("capstone/salon/virtual/RPM",str(rpm)) # Publish message to MQTT broker
    sleep(SAMPLE_TIME) # Tiempo de espera entre cada lectura
    

print("Fin del programa, ¡¡¡Saludos!!!")
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.cleanup() # Limpiamos todos los pines
