# Control de un motor de corriente directa, variando su voltaje por mqtt
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

while True:
    x=input("% del voltaje\n")
    z=int(x) # Convertimos el valor de str de x a int (entero)
    print(x)
    if z == -1: # Para salirnos del ciclo
        p.ChangeDutyCycle(0) 
        break
    p.ChangeDutyCycle(z) # Cambiamos el porcentaje de voltaje (0-100)


print("Fin del programa, ¡¡¡Saludos!!!")
#Para asegurarnos de apagar el motor
GPIO.output(in1,GPIO.LOW) 
GPIO.output(in2,GPIO.LOW)
GPIO.cleanup() # Limpiamos todos los pines

