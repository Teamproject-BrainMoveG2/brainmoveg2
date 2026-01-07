// Wifi code
#include "WiFi.h"
#include <HTTPClient.h>
#include "secrets.h"
// TOF code
#include <Wire.h>
#include "Adafruit_VL53L0X.h"

Adafruit_VL53L0X lox;

// Buzzer code
const int BUZZER_PIN = D3;

// RGB code
int roodLed = A0;
int blauwLed = A1;
int groenLed = A2;

void setup()
{
  Serial.begin(115200);
  delay(1000);
  // Wifi code
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  uint8_t r = WiFi.waitForConnectResult();
  Serial.printf("result=%d status=%d ip=%s\n",
                r, WiFi.status(),
                WiFi.localIP().toString().c_str());

  Serial.print("Verbinden met WiFi");
  // Buzzer code
  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(BUZZER_PIN, LOW);
  // TOF code
  Wire.begin();

  if (!lox.begin()) {
    Serial.println("Failed to boot VL53L0X");
    while (1) delay(10);
  }

  // RGB code
  pinMode(roodLed, OUTPUT);
  pinMode(blauwLed, OUTPUT);
  pinMode(groenLed, OUTPUT);
}

void loop()
{
  // Wifi code
  wifi();

  // buzzer code
  beep(2, 100, 100);
  delay(1000);
  beep(1, 500, 100);
  delay(2000);

  // TOF code
  //  tof();

  // RGB code
  //  Rood
  digitalWrite(roodLed, LOW);
  digitalWrite(groenLed, HIGH);
  digitalWrite(blauwLed, HIGH);
  delay(500);

  // Groen
  digitalWrite(roodLed, HIGH);
  digitalWrite(groenLed, LOW);
  digitalWrite(blauwLed, HIGH);
  delay(500);

  // Blauw
  digitalWrite(roodLed, HIGH);
  digitalWrite(groenLed, HIGH);
  digitalWrite(blauwLed, LOW);
  delay(500);
}

// Buzzer code
void beep(int times, int on_ms, int off_ms)
{
  for (int i = 0; i < times; i++)
  {
    digitalWrite(BUZZER_PIN, HIGH);
    delay(on_ms);
    digitalWrite(BUZZER_PIN, LOW);
    delay(off_ms);
  }
}
// TOF code
void tof()
{
  VL53L0X_RangingMeasurementData_t measure;

  lox.rangingTest(&measure, false);

  if (measure.RangeStatus != 4)
  {
    Serial.print("Distance (mm): ");
    Serial.println(measure.RangeMilliMeter);
    if (measure.RangeMilliMeter < 300)
    {
      Serial.println("potje gedetecteerd");
    }
  }
  else
  {
    Serial.println("Out of range");
  }
}

// Wifi code
void wifi()
{
  Serial.print(WiFi.status());
  if (WiFi.status() == WL_CONNECTED)
  {
    Serial.println("\nVerbonden! IP-adres: ");
    Serial.println(WiFi.localIP());
    delay(500); // Print elke 5 sec
  }
  else
  {
    Serial.print(".");
    delay(100);
  }
}

// #include <WiFi.h>
// #include <HTTPClient.h>
// #include "Adafruit_VL53L0X.h"

// const char* ssid = "JOUW_RPI_HOTSPOT";
// const char* password = "JOUW_WACHTWOORD";
// const char* rpiUrl = "http://192.168.4.1/api/distance";  // RPi endpoint

// void setup() {
//   Serial.begin(115200);
//   pinMode(A0, INPUT);
//   while (!Serial) delay(1);

//   Wire.begin();  // I2C op defaults GPIO2/3
//   if (!lox.begin()) {
//     Serial.println("VL53L0X boot falen!");
//     while(1);
//   }
//   Serial.println("VL53L0X klaar!");

//   WiFi.begin(ssid, password);
//   while (WiFi.status() != WL_CONNECTED) {
//     delay(1000);
//     Serial.print(".");
//   }
//   Serial.println("\nWiFi verbonden!");
// }

// void loop() {
//   VL53L0X_RangingMeasurementData_t measure;
//   lox.rangingTest(&measure, false);

//   if (measure.RangeStatus != 4) {
//     int distance = measure.RangeMilliMeter;
//     Serial.print("Afstand: "); Serial.print(distance); Serial.println(" mm");

//     if (WiFi.status() == WL_CONNECTED) {
//       HTTPClient http;
//       http.begin(rpiUrl);
//       http.addHeader("Content-Type", "application/json");
//       String postData = "{\"distance\":" + String(distance) + "}";
//       int httpCode = http.POST(postData);
//       if (httpCode > 0) Serial.printf("Verzonden, code: %d\n", httpCode);
//       http.end();
//     }
//   } else {
//     Serial.println("Out of range");
//   }
//   uint32_t Vbatt = 0;
//   for(int i = 0; i < 16; i++) {
//     Vbatt = Vbatt + analogReadMilliVolts(A0); // ADC with correction
//   }
//   float Vbattf = 2 * Vbatt / 16 / 1000.0;     // attenuation ratio 1/2, mV --> V
//   Serial.println(Vbattf, 3);
//   delay(1000);
//   delay(1000);
// }
