# Control de un motor de corriente directa, variando su voltaje
# Este script mide la velocidad
# Por: Francisco Alejandro Alaffita Hernández
# Fecha: 17 de junio de 2022
#
# Raspberry     L298N
#     23  -------In2
#     24  -------In1
#     25  -------en
#     GND -------GND

import RPi.GPIO as GPIO          
from time import sleep
import pigpio
from read_RPM import reader
import numpy as np
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

#Iniciamos el motor de dc con el 0% del voltaje total (12 v) 
 
GPIO.output(in1,GPIO.HIGH)
GPIO.output(in2,GPIO.LOW)
p.ChangeDutyCycle(0)


# Set up RPM reader
RPM_GPIO = 6 # Pin del que vamos a leer
SAMPLE_TIME = 0.01 # Tiempo de muestreo
pi = pigpio.pi() # Creación de nuestra variable para las RPM
# pi.set_servo_pulsewidth(6, 2000) # Maximum throttle.
# sleep(2)
# pi.set_servo_pulsewidth(6, 1000) # Minimum throttle.
# sleep(2)

tach = reader(pi, RPM_GPIO,334,0,0) # Creación de la clase reader, el 334 son los pulsos por ciclo

Vin=12
b=7.10639123732791
c=(81088.9809185961)*Vin/12
k1=0;
k2=0;
A=np.array([[1,1],[0,-b]])
B=np.array([[k1],[k2-c/b]])
invA=np.linalg.inv(A)
CC=np.dot(invA,B)
# Recuerda que los indices comienzan en 0, así que CC[1] es CC[2]
# en matlab
t=0;
dy=(c/b)-b*CC[1]*np.exp(-b*t)
print(dy)
# dy=(c/b)-b*CC(2)*exp(-b*t);

#Simulación por ecuaciones diferenciales




i=0
x=100
while i<200:
    #x=input("% del voltaje\n") # Pedimos un porcentaje o v para la velocidad o -1 salir
#    z=int(x) # Convertimos el valor de str de x a int (entero)
    #print(x)
    #if x == '-1': # Para salirnos del ciclo
    #    p.ChangeDutyCycle(0) 
    #    break
    #elif x == 'v': # Medir una vez la velocidad
    rpm = tach.RPM() # Aqui es donde obtenemos la interrupcion para medir la velocidad
    print(rpm)
    sleep(SAMPLE_TIME)
    #    break
    p.ChangeDutyCycle(int(x)) # Cambiamos el porcentaje de voltaje (0-100)
    i=i+1
    dy=(c/b)-b*CC[1]*np.exp(-b*t)
    print(dy[0])
    t=t+0.01;

print("Fin del programa, ¡¡¡Saludos!!!")
#Para asegurarnos de apagar el motor
GPIO.output(in1,GPIO.LOW) 
GPIO.output(in2,GPIO.LOW)
GPIO.cleanup() # Limpiamos todos los pines
pi.stop() # Disconnect pigpio.