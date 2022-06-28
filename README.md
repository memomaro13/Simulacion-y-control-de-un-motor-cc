Este repositorio forma parte del curso IoT de Samsung Innovation Campus
El objetivo es el control de un motor de corriente contínua por wifi

Está organizado de la siguiente manera:

# Curso:
      Esta carpeta contiene los documentos para hacer las conexiones y cada una de las lecciones para lograr hacer el circuito y los programas para controlar el motor de corriente contínua.
      
      1. Conectando la Raspberry pi 4 al módulo L298N y motor de Corriente directa
      2. Medir velocidad desde el encoder del motor
      3. Control del Motor via MQTT
      4. Conectando una pantalla Oled a Raspberry Pi

# Imagenes:
      Contiene todas las imagenes y los circuitos usadas en los documentos que se encuentran en la carpeta Curso en formato png y de fritzing en el caso de los circuitos.

# Python:
      Contiene los programas en python de manera desglosada, es decir, dependiendo en que etapa te encuentres del curso es el archivo necesario, es decir, 
      
      >si vas a conectar el motor entonces necesitas el archivo: solo_motor_raspberry.py
      >si vas a conectar el encoder y el motor necesitas el archivo: velocidad_RPM.py y read_RPM.py
      >si vas a controlar el motor desde mqtt necesitas el archivo: velocidad_voltaje_mqtt.py
      >si vas a conectar sólo la pantalla necesitas el archivo: pantalla_oled.py



Este repositorio contiene todos los archivos necesarios para llevar a cabo el proyecto capstone: "Control y simulación de un motor de corriente contínua por wifi".
![This is an image](https://raw.githubusercontent.com/AlexAlaffita/Simulacion-y-control-de-un-motor-cc/main/Imagenes/circuito_motor_encoder_L298N_pantalla_bb.png)
