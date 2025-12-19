// Pin donde está conectado el potenciómetro
const int pinPot = A0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  // Leer el valor del potenciómetro (0 - 1023)
  int lectura = analogRead(pinPot);

  // Mapear el valor a un rango de 1 a 100
  int valor = map(lectura, 180, 860, 1, 100);

  // Enviar solo el número, seguido de salto de línea
  Serial.println(valor);

  // Pequeña pausa para no saturar el puerto serie
  delay(100);
}
