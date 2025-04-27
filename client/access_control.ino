#include <Servo.h>
#include <WiFiNINA.h>
#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9
#define SERVO_PIN 6
#define RED_PIN 3
#define GREEN_PIN 2
MFRC522 mfrc522(SS_PIN, RST_PIN);
Servo servo;
char ssid[] = "myssd";
char pass[] = "pypasswd";
int status = WL_IDLE_STATUS;
char server[] = "192.168.1.219";
WiFiClient client;

void setup() {
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
  if (WiFi.status() == WL_NO_MODULE) {
    Serial.println("Module is unresponsive");
    while (true)
      ;
  }
  while (status != WL_CONNECTED) {
    Serial.println("Attempting connection...");
    status = WiFi.begin(ssid, pass);
    delay(10000);
  }
  IPAddress ip = WiFi.localIP();
  Serial.println(ip);
  servo.attach(SERVO_PIN);
  servo.write(45);
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
}

void loop() {
  if (!mfrc522.PICC_IsNewCardPresent()) return;
  if (!mfrc522.PICC_ReadCardSerial()) return;
  char content[mfrc522.uid.size + 1];
  Serial.println("Tag: ");
  for (int i = 0; i < mfrc522.uid.size; i++) {
    byte b = mfrc522.uid.uidByte[i];
    Serial.print(b < 0x10 ? " 0" : " ");
    Serial.print(b, HEX);
    content[i] = b;
  }
  content[mfrc522.uid.size - 1] = 0;
  if (client.connect(server, 5000)) {
    client.print("GET /iskeyvalid?id=");
    client.println(content);
    client.println("Host: 192.168.1.219");
    client.println("Connection: close");
    client.println();
  }

  while (!client.available()) delay(5);
  char c;
  while (client.available()) c = client.read();
  if (c == 'r') {
    digitalWrite(RED_PIN, HIGH);
    delay(1000);
    digitalWrite(RED_PIN, LOW);
  } else if (c == 'a') {
    digitalWrite(GREEN_PIN, HIGH);
    delay(200);
    digitalWrite(GREEN_PIN, LOW);
    delay(200);
    digitalWrite(GREEN_PIN, HIGH);
    delay(200);
    digitalWrite(GREEN_PIN, LOW);
  } else if (c == 'g') {
    digitalWrite(GREEN_PIN, HIGH);
    servo.write(135);
    delay(1000);
    digitalWrite(GREEN_PIN, LOW);
    delay(4000);
    servo.write(45);
  }
}