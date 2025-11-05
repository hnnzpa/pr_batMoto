import serial
import time

'''
class ArduinoReader:
    def __init__(self, port='COM5', baudrate=9600):
        self.arduino = serial.Serial(port=port, baudrate=baudrate, timeout=1)
        time.sleep(2)  # Esperar a que se inicie la conexión

    def leer_valor(self):
        if self.arduino.in_waiting > 0:
            linea = self.arduino.readline().decode('utf-8').strip()
            if linea.isdigit():
                return int(linea)
        return None

    def cerrar(self):
        self.arduino.close()
'''
arduino = serial.Serial(port="COM5", baudrate=9600, timeout=1)
time.sleep(2)  # esperar a que Arduino reinicie

def leer_arduino():
    while True:
        line = arduino.readline().decode('utf-8', errors='ignore').strip()
        
        if line:  # si la línea no está vacía
            try:
                valor = int(line)
                return valor
            except ValueError:
                print(f"⚠️ Dato inválido recibido: '{line}' (no es un entero)")
        else:
            # si está vacía, esperamos un poco y volvemos a intentar
            time.sleep(0.01)