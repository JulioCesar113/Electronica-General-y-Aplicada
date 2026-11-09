#include <SoftwareSerial.h>

int motorIzqPinA = 2; // IN2
int motorIzqPinB = 4; // IN1
int motorDerPinA = 7; // IN4
int motorDerPinB = 5; // IN3
int velocidadIzqPin = 6;  
int velocidadDerPin = 3;  

SoftwareSerial bluetooth(10, 11); 

void setup() {
  Serial.begin(9600);
  bluetooth.begin(9600);
  
  pinMode(motorIzqPinA, OUTPUT);
  pinMode(motorIzqPinB, OUTPUT);
  pinMode(motorDerPinA, OUTPUT);
  pinMode(motorDerPinB, OUTPUT);
  pinMode(velocidadIzqPin, OUTPUT);
  pinMode(velocidadDerPin, OUTPUT);
}

void loop() {
  if (bluetooth.available()) {
    String mensaje = bluetooth.readStringUntil('\n');
    
    char x, y;
    int vel;
    
    if (sscanf(mensaje.c_str(), "%c, %c, %d", &x, &y, &vel) == 3) {
      aplicarMovimiento(x, y, vel);
    }
     int datosLeidos = sscanf(mensaje.c_str(), "%c, %c, %d", &x, &y, &vel);
if (datosLeidos == 3) {
  vel = map(vel, 0, 100, 0, 255);
  aplicarMovimiento(x, y, vel);
  Serial.print("Eje X: "); Serial.println(x);
  Serial.print("Eje Y: "); Serial.println(y);
  Serial.print("Velocidad: "); Serial.println(vel);
  Serial.println("-----------------");
}
}
}
void aplicarMovimiento(char x, char y, int vel) {
  // 1. Control del eje Y (Avance y Retroceso)
  if (y == 'F') { // Adelante
    digitalWrite(motorIzqPinA, HIGH);
    digitalWrite(motorIzqPinB, LOW);
    digitalWrite(motorDerPinA, HIGH);
    digitalWrite(motorDerPinB, LOW);
  } else if (y == 'B') { // Atrás
    digitalWrite(motorIzqPinA, LOW);
    digitalWrite(motorIzqPinB, HIGH);
    digitalWrite(motorDerPinA, LOW);
    digitalWrite(motorDerPinB, HIGH);
  } else { // Neutral
    digitalWrite(motorIzqPinA, LOW);
    digitalWrite(motorIzqPinB, LOW);
    digitalWrite(motorDerPinA, LOW);
    digitalWrite(motorDerPinB, LOW);
  }

  // 2. Control de la velocidad por PWM
  int pwmIzq = vel;
  int pwmDer = vel;

  if (x == 'L') {
    pwmIzq = 0; 
  } else if (x == 'R') {
    pwmDer = 0; 
  }

  // Frenado total si no hay teclas presionadas
  if (y == 'N' && x == 'N') {
    pwmIzq = 0;
    pwmDer = 0;
  }

  analogWrite(velocidadIzqPin, pwmIzq);
  analogWrite(velocidadDerPin, pwmDer);
}
