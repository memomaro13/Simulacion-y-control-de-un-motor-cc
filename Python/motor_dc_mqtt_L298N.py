import paho.mqtt.client as mqtt # Import the MQTT library
import RPi.GPIO as GPIO          
from time import sleep
import pigpio
from read_RPM import reader # Archivo read_RPM contiene a la clase reader

def messageFunction (client, userdata, message):
    topic = str(message.topic)
    message = int(message.payload.decode("utf-8"))
    print(message)
    p.ChangeDutyCycle(message)

broker_address="35.157.61.99" # IP de hivemq
ourClient = mqtt.Client("makerio_mqtt") # Create a MQTT client object
ourClient.connect(broker_address, 1883) # Connect to the test MQTT broker
ourClient.subscribe("house/bulbs/bulb1") # Subscribe to the topic AC_unit
ourClient.on_message = messageFunction # Attach the messageFunction to subscription
ourClient.loop_start() # Start the MQTT client

# Pines de conexión con el shield L298N
in1 = 24 
in2 = 23
en = 25


GPIO.setmode(GPIO.BCM) # Para fijar el modo para los pines

GPIO.setup(in1,GPIO.OUT) # Definimos a in1 como de salida
GPIO.setup(in2,GPIO.OUT) # Definimos a in2 como de salida
GPIO.setup(en,GPIO.OUT)  # Definimos a en como de salida
GPIO.output(in1,GPIO.LOW)# Para estar seguros que el motor se detiene antes de comenzar 
GPIO.output(in2,GPIO.LOW)# Para estar seguros que el motor se detiene antes de comenzar
p=GPIO.PWM(en,1000) # La frecuencia para el pulso PWM en el pin en, de la variable p
p.start(25) # Para comenzar con el 25% con el movimiento del motor
print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
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

#Iniciamos el motor de dc con el 25% del voltaje total (12 v) 
 
GPIO.output(in1,GPIO.HIGH)
GPIO.output(in2,GPIO.LOW)
p.ChangeDutyCycle(25)
x='1'
while(1):
        
    rpm = tach.RPM() # Función para leer las rpm
    print(rpm)
    ourClient.subscribe("capstone/salon/virtual/voltaje") # Subscribe message to MQTT broker
    ourClient.publish("capstone/salon/virtual/RPM",str(rpm)) # Publish message to MQTT broker
    sleep(SAMPLE_TIME) # Tiempo de espera entre cada lectura
#    if x=='1':
#        break
print("stop")
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.cleanup() # Limpiamos todos los pines
