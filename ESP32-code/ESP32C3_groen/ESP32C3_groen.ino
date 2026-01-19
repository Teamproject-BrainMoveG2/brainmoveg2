// Wifi code
#include "WiFi.h"
#include <HTTPClient.h>
#include "secrets.h"
// TOF code
#include <Wire.h>
#include "Adafruit_VL53L0X.h"

Adafruit_VL53L0X lox;

static bool tofArmed = true;            // mag er een nieuwe hit komen?
static const uint16_t HIT_MM = 150;     // detectiedrempel
static const uint16_t RELEASE_MM = 180; // loslaat-drempel (hysteresis)
static unsigned long lastHitMs = 0;
static const unsigned long HIT_COOLDOWN_MS = 300; // extra bescherming tegen dubbel triggeren

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

const char *url = "http://10.42.0.1:8000/"; // <-- RPi hotspot IP

void setup()
{
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
  if (!lox.begin())
  {
    Serial.println("Failed to boot VL53L0X");
    // Fail-safe: buzzer/led indicatie en stop
    while (true)
    {
      delay(1000);
    }
  }

  // WiFi init (met timeout)
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Verbinden met WiFi");

  uint32_t t0 = millis();
  while (WiFi.status() != WL_CONNECTED && (millis() - t0) < 10000)
  {
    Serial.print(".");
    delay(250);
  }

  if (WiFi.status() == WL_CONNECTED)
  {
    Serial.printf("\nWiFi OK, IP=%s RSSI=%d\n",
                  WiFi.localIP().toString().c_str(),
                  WiFi.RSSI());
  }
  else
  {
    Serial.println("\nWiFi FAIL (timeout)");
    // Hier kan je beslissen: verder zonder WiFi, of resetten, of blijven proberen.
  }
  // batterij code
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
  if (now - lastBatteryMs >= BATTERY_INTERVAL_MS)
  {
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

  bool valid = (measure.RangeStatus != 4); // jouw "geldige meting" check
  uint16_t d = measure.RangeMilliMeter;

  if (valid)
  {
    Serial.print("Distance (mm): ");
    Serial.println(d);
  }
  else
  {
    Serial.println("Out of range");
  }

  // Re-arm: pas als er echt niets meer dichtbij is (of meting ongeldig)
  if (!valid || d > RELEASE_MM)
  {
    tofArmed = true;
  }

  // Trigger: alleen als we "armed" zijn én we nu dichtbij detecteren
  if (tofArmed && valid && d < HIT_MM && (millis() - lastHitMs) > HIT_COOLDOWN_MS)
  {
    tofArmed = false;
    lastHitMs = millis();

    Serial.println("potje gedetecteerd");

    HTTPClient http;
    String hitUrl = String(url) + "games/hit";
    http.begin(hitUrl);
    http.addHeader("Content-Type", "application/json");
    String payload = String("{\"cone_id\":\"") + KLEUR + "\"}";
    http.POST(payload);
    http.end();
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
void lees_batterij()
{
  uint32_t Vsum_mV = 0;
  for (int i = 0; i < 16; i++)
    Vsum_mV += analogReadMilliVolts(batterij); // mV op ADC pin (gekalibreerd)

  float Vadc = (Vsum_mV / 16.0f) / 1000.0f; // V op ADC pin
  float Vbat = 2.0f * Vadc;                 // 1/2 spanningsdeler -> batterijspanning

  float bat_procent_f = (Vbat - 3.0f) / (4.2f - 3.0f) * 100.0f; // 3.0V=0%, 4.2V=100%
  bat_procent_f = constrain(bat_procent_f, 0.0f, 100.0f);

  int bat_procent = (int)(bat_procent_f + 0.5f);

  Serial.printf("batterij=%d%%\n", bat_procent);
  Serial.printf("Vadc=%.3fV\nVbat=%.3fV\n", Vadc, Vbat);
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

void setRgb(bool rOn, bool gOn, bool bOn)
{
  digitalWrite(roodLed, rOn ? LOW : HIGH);
  digitalWrite(groenLed, gOn ? LOW : HIGH);
  digitalWrite(blauwLed, bOn ? LOW : HIGH);
}

void setLedByBattery(int percent)
{
  percent = constrain(percent, 0, 100);

  if (percent >= 60)
  {
    setRgb(false, true, false); // groen
  }
  else if (percent >= 25)
  {
    setRgb(true, true, false); // geel (rood+groen)
  }
  else
  {
    setRgb(true, false, false); // rood
  }
}
