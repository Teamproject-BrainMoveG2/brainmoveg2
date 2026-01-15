// Wifi code
#include "WiFi.h"
#include <HTTPClient.h>
#include "secrets.h"
// TOF code
#include <Wire.h>
#include "Adafruit_VL53L0X.h"

Adafruit_VL53L0X lox;

// Buzzer code
const int BUZZER_PIN = D6;

// Batterij code
int batterij = A0;
unsigned long lastBatteryMs = 0;
const unsigned long BATTERY_INTERVAL_MS = 30000;

// RGB code
int roodLed = A1;
int blauwLed = D3;
int groenLed = A2;

const char* url = "http://10.42.0.1:8000/"; // <-- RPi hotspot IP

void setup() {
  Serial.begin(115200);
  delay(200);

  // Pins eerst in een veilige toestand zetten
  pinMode(roodLed, OUTPUT);
  pinMode(groenLed, OUTPUT);
  pinMode(blauwLed, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  digitalWrite(BUZZER_PIN, LOW);

  // I2C + sensor init
  Wire.begin();
  if (!lox.begin()) {
    Serial.println("Failed to boot VL53L0X");
    // Fail-safe: buzzer/led indicatie en stop
    while (true) { delay(1000); }
  }

  // WiFi init (met timeout)
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Verbinden met WiFi");

  uint32_t t0 = millis();
  while (WiFi.status() != WL_CONNECTED && (millis() - t0) < 10000) {
    Serial.print(".");
    delay(250);
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.printf("\nWiFi OK, IP=%s RSSI=%d\n",
                  WiFi.localIP().toString().c_str(),
                  WiFi.RSSI());
  } else {
    Serial.println("\nWiFi FAIL (timeout)");
    // Hier kan je beslissen: verder zonder WiFi, of resetten, of blijven proberen.
  }
  //batterij code
  lees_batterij();
}


void loop()
{
  // Wifi code
  wifi();

  // buzzer code
  // beep(2, 100, 100);
  // delay(1000);
  // beep(1, 500, 100);
  // delay(2000);

  // TOF code
  tof();
 
  unsigned long now = millis();
  if (now - lastBatteryMs >= BATTERY_INTERVAL_MS) {
    lastBatteryMs = now;
    lees_batterij();
  }
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
    if (measure.RangeMilliMeter < 150)
    {
      Serial.println("potje gedetecteerd");
      HTTPClient http;
      String hitUrl = String(url) + "games/hit";
      http.begin(hitUrl);
      http.addHeader("Content-Type", "application/json");

      String payload = String("{\"cone_id\":\"") + KLEUR + "\"}";

      int code = http.POST(payload);
      delay(1000);
      // Serial.printf("POST status: %d\n", code);

      http.end();
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

    // HTTPClient http;
    // String hitUrl = String(url) + "cone/connect";
    // http.addHeader("Content-Type", "application/json"); // JSON content-type

    // String payload = String("{\"batterij\":\"") + bat_procent + "\"}";
    // int code = http.POST(payload); // POST request

    // http.end();
  }
  else
  {
    Serial.print(".");
    // delay(100);
  }
}
void lees_batterij() {
  uint32_t Vsum_mV = 0;

  for (int i = 0; i < 16; i++) {
    Vsum_mV += analogReadMilliVolts(batterij);  // mV (gekalibreerd)
  }

  float Vadc = (Vsum_mV / 16.0f) / 1000.0f;     // mV -> V
  float Vbat = 2.0f * Vadc;                     // spanningsdeler 1/2 (pas aan indien anders!)

  float bat_procent_f = (Vadc / 3.3f) * 100.0f;
  bat_procent_f = constrain(bat_procent_f, 0.0f, 100.0f);

  int bat_procent = (int)(bat_procent_f + 0.5f);

  Serial.printf("batterij=%d%%\n", bat_procent);
  setLedByBattery(bat_procent);
  
  HTTPClient http;
  String statusUrl = String(url) + "cones/status";
  http.begin(statusUrl);
  http.addHeader("Content-Type", "application/json");

  String payload =
  String("{\"cone_id\":\"") + KLEUR +
  String("\",\"battery_percentage\":") + bat_procent +
  String("}");

  int code = http.POST(payload);

  http.end();  
}

void setRgb(bool rOn, bool gOn, bool bOn) {
  digitalWrite(roodLed,  rOn ? LOW : HIGH);
  digitalWrite(groenLed, gOn ? LOW : HIGH);
  digitalWrite(blauwLed, bOn ? LOW : HIGH);
}

void setLedByBattery(int percent) {
  percent = constrain(percent, 0, 100);

  if (percent >= 60) {
    setRgb(false, true, false);   // groen
  } else if (percent >= 25) {
    setRgb(true, true, false);    // geel (rood+groen)
  } else {
    setRgb(true, false, false);   // rood
  }
}
