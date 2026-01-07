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

const char* url = "http://10.42.0.1:8000/ingest"; // <-- RPi hotspot IP

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
  // Wire.begin();

  // if (!lox.begin()) {
  //   Serial.println("Failed to boot VL53L0X");
  //   while (1) delay(10);
  // }

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
  // Serial.print(WiFi.status());
  if (WiFi.status() == WL_CONNECTED)
  {
    // Serial.println("\nVerbonden! IP-adres: ");
    // Serial.println(WiFi.localIP());
    // delay(500); // Print elke 5 sec
    HTTPClient http;
    http.begin(url);
    http.addHeader("Content-Type", "application/json"); // JSON content-type

    String payload =
      String("{\"device\":\"esp32-c3\",\"ms\":\"") + String(millis()) +
      String("\",\"rssi\":\"") + String(WiFi.RSSI()) +
      String("\",\"ip\":\"") + WiFi.localIP().toString() + String("\"}");
    Serial.print(payload);
    int code = http.POST(payload); // POST request
    Serial.printf("POST status: %d\n", code);

    http.end();
  }
  else
  {
    Serial.print(".");
    delay(100);
  }
}
