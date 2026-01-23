// MQTT code
#include <ArduinoJson.h>
#include <PubSubClient.h>

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

// MQTT Configuration
const char *MQTT_SERVER = "10.42.0.1"; // RPi hotspot IP
const int MQTT_PORT = 1883;
WiFiClient espClient;
PubSubClient mqttClient(espClient);
String mqtt_topic_buzzer;

// Buzzer code
const int BUZZER_PIN = D6;

static unsigned long buzzerOnUntil = 0;
static unsigned long buzzerOffUntil = 0;
static int buzzerBeepsLeft = 0;
static int buzzerDuration = 0;
static int buzzerPause = 0;

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
  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(BUZZER_PIN, LOW);

  Serial.begin(115200);
  delay(200);

  // Pins eerst in een veilige toestand zetten
  pinMode(roodLed, OUTPUT);
  pinMode(groenLed, OUTPUT);
  pinMode(blauwLed, OUTPUT);

  // I2C + sensor init
  Wire.begin();

  if (!lox.begin())
  {
    Serial.println("Failed to boot VL53L0X");
    // Fail-safe: led indicatie en stop
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
  // MQTT code
  setup_mqtt();

  // batterij code
  lees_batterij();
}

void loop()
{
  //buzzer code
  update_buzzer();
  
  // MQTT
  if (WiFi.status() == WL_CONNECTED)
  {
    reconnect_mqtt();
    mqttClient.loop();
  }

  // TOF code
  tof();

  unsigned long now = millis();
  if (now - lastBatteryMs >= BATTERY_INTERVAL_MS)
  {
    lastBatteryMs = now;
    lees_batterij();
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
    trigger_buzzer_pattern("single", 50);
  }
}

// Batterij code
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

// RGB code
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

// MQTT code
void setup_mqtt()
{
  mqtt_topic_buzzer = String("brainmove/cones/") + KLEUR + "/buzzer";
  mqttClient.setServer(MQTT_SERVER, MQTT_PORT);
  mqttClient.setCallback(mqtt_callback);
}

void mqtt_callback(char *topic, byte *payload, unsigned int length)
{
  StaticJsonDocument<200> doc;
  deserializeJson(doc, payload, length);

  String action = doc["action"];
  String pattern = doc["pattern"];
  int duration = doc["duration_ms"];

  if (action == "beep")
  {
    trigger_buzzer_pattern(pattern, duration);
  }
}
 // Buzzer code
void trigger_buzzer_pattern(String pattern, int duration)
{
  buzzerBeepsLeft = 0;
  buzzerDuration = duration;
  buzzerPause = 100;
  if (pattern == "single")
    buzzerBeepsLeft = 1;
  else if (pattern == "double")
    buzzerBeepsLeft = 2;
  else if (pattern == "triple")
    buzzerBeepsLeft = 3;
  buzzerOnUntil = millis() + buzzerDuration; // Start immediately
}
// MQTT reconnect
void reconnect_mqtt()
{
  if (!mqttClient.connected())
  {
    String clientId = String("ESP32-") + KLEUR; // concat hier
    if (mqttClient.connect(clientId.c_str()))
    {
      mqttClient.subscribe(mqtt_topic_buzzer.c_str());
      Serial.println("MQTT Connected and subscribed to: " + mqtt_topic_buzzer);
    }
  }
}
// Buzzer code
void update_buzzer()
{
  unsigned long now = millis();
  if (buzzerOnUntil > 0)
  {
    if (now < buzzerOnUntil)
    {
      digitalWrite(BUZZER_PIN, HIGH);
    }
    else
    {
      digitalWrite(BUZZER_PIN, LOW);
      buzzerOnUntil = 0;
      buzzerOffUntil = now + buzzerPause;
    }
  }
  else if (buzzerOffUntil > 0)
  {
    if (now >= buzzerOffUntil)
    {
      buzzerOffUntil = 0;
      if (--buzzerBeepsLeft > 0)
      {
        buzzerOnUntil = now + buzzerDuration;
      }
    }
  }
}