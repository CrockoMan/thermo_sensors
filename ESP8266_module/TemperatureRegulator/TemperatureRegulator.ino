#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <Ticker.h>
#include <EncButton.h>
#include <EEPROM.h>
#include <GyverSegment.h>
#include <GyverRelay.h>
#include <microDS18B20.h>
#include <StringUtils.h>
#include <GSON.h>
#include "settings.h"


#define SHOW_TEMP 0
#define SET_TEMP 1
#define SHOW_TARGET_TEMP 2
#define ADJUST_TARGET_TEMP 3

#define MIN_SENSOR_VALUE 18
#define MAX_SENSOR_VALUE 35

#define TEMP_READ_INTERVAL_x10ms 5

//#define SERVER_POST_MESSAGE_INTERVAL_x10ms 10*10
#define SERVER_POST_MESSAGE_INTERVAL_x10ms 60*10


#define LED_PIN 16
#define LED_ON  digitalWrite(16, LOW)
#define LED_OFF digitalWrite(16, HIGH)

#define RELAY_PIN 0
#define RELAY_OFF digitalWrite(0, HIGH)
#define RELAY_ON  digitalWrite(0, LOW)

#define DIO_PIN 4
#define CLK_PIN 5
//#define LAT_PIN 4
Disp1637_4 disp(DIO_PIN, CLK_PIN);

#define TEMP_SENSOR_PIN 2
MicroDS18B20<TEMP_SENSOR_PIN> sensor1;
// GyverRelay regulator(REVERSE);
GyverRelay regulator(NORMAL);

Ticker Timer;

volatile unsigned char TimerTick=0, LedTimerTicker=0, isTicker=0,
                       CustomTimerTicker=0, SensorTimer=0, ReadTempComplete=0;
volatile unsigned int http_timer=0;
char CurrentTemp;
unsigned char TempTimer, Brightness, WiFiConnected, CurrentMode=SHOW_TEMP;
float TempFloat=0, TargetTemp=29;


EncButton eb(13, 12, 14);
// пин CLK, пин DT, пин SW, тип
// EncButton eb(2, 3, 4, INPUT); // + режим пинов энкодера
// EncButton eb(2, 3, 4, INPUT, INPUT_PULLUP); // + режим пинов кнопки


// CLK D1   DIO D2

void timerIsr()
{
  unsigned char TimerTicker;
  isTicker=1;
  if(WiFiConnected) TimerTicker = 10;
  else              TimerTicker = 2;
  if( TimerTick<TimerTicker ) TimerTick++;
  else                        TimerTick=0;

  if(LedTimerTicker<10) LedTimerTicker++;
  else                  LedTimerTicker = 0;

  if(CustomTimerTicker<10) CustomTimerTicker++;
  else                     CustomTimerTicker = 0;

  if(SensorTimer<TEMP_READ_INTERVAL_x10ms)  SensorTimer++;
  else
  {
    SensorTimer=0;
    TempFloat=sensor1.getTemp();
    sensor1.requestTemp();
    CurrentTemp=TempFloat;
    regulator.input = TempFloat;                      // сообщаем регулятору текущую температуру
    digitalWrite(RELAY_PIN, regulator.getResult());   // отправляем на реле (ОС работает по своему таймеру)
    ReadTempComplete=1;
  }
  http_timer++;
}


void SaveSettings()
{
    EEPROM.begin(512);
    EEPROM.write(0, TargetTemp);
    EEPROM.write(1, Brightness);
    EEPROM.commit();

    regulator.setpoint = TargetTemp;
}


void CheckAndSaveSettings()
{
  if(TargetTemp<MIN_SENSOR_VALUE || TargetTemp>MAX_SENSOR_VALUE)
  {
    TargetTemp = MIN_SENSOR_VALUE + (MAX_SENSOR_VALUE-MIN_SENSOR_VALUE)/2;
    SaveSettings();
  }
  if(Brightness>7)
  {
    Brightness = 1;
    SaveSettings();
  }
}

unsigned char ReadTemp()
{
    EEPROM.begin(512);
    TargetTemp = EEPROM.read(0);
    return(TargetTemp);
}

unsigned char ReadBrightness()
{
    EEPROM.begin(512);
    Brightness = EEPROM.read(1);
    return(Brightness);
}

void ShowTemp(float Temp)
{
  disp.brightness(Brightness);
  disp.setCursor(0);
  if(Temp<9)
  {
      disp.print(" ");
  }
  disp.print(Temp);
  disp.setCursor(3);
  disp.print("*");
  if(CurrentMode == ADJUST_TARGET_TEMP && LedTimerTicker>=5)
  {
    disp.setCursor(3);
    disp.print(" ");
  }
  disp.update();
}



void setup() {
  int address = 0;
  byte value_w;
  unsigned char connect_attempt = 10;
  CurrentTemp = 22;

  pinMode(RELAY_PIN, OUTPUT);
  RELAY_OFF;
  pinMode(LED_PIN, OUTPUT);
  Timer.attach(0.1, timerIsr);


  sensor1.setResolution(9);
  sensor1.requestTemp();


  Serial.begin(115200);
  Serial.println("");

//--------------------------------------------------- Чтение уставки температуры
  TargetTemp = ReadTemp();
  Brightness = ReadBrightness();
  CheckAndSaveSettings();


// Инициализация регулятора
  regulator.setpoint = TargetTemp;
  regulator.hysteresis = 0.2; // ширина гистерезиса
  regulator.k = 0.5;          // коэффициент обратной связи (подбирается по факту)


  Serial.println();
  Serial.print("Установленная температура: ");
  Serial.println(TargetTemp);
  Serial.print("Установленная яркость: ");
  Serial.println(Brightness);
  ShowTemp(TargetTemp);
//--------------------------------------------------- Чтение уставки температуры

  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while ( WiFi.status() != WL_CONNECTED && connect_attempt>0) 
  {
    delay(500);
    Serial.print(".");
    connect_attempt--;
  }
  if(WiFi.status() != WL_CONNECTED) WiFiConnected = false;
  else                              WiFiConnected = true;

  if(WiFiConnected)
  {
    Serial.println("WiFi Connected");
    Serial.println(WiFi.localIP());
    get_settings();
  }
  else
  {
    Serial.println("WiFi Connection ERROR");
  }

  eb.setEncReverse(1);


  ShowTemp(CurrentTemp);  // Вывод текущей температуры

}


void post_measurement(float temp)
{
  gson::string gs;

    // Формирование JSON 
    gs.beginObj();
    gs["username"] = USER_LOGIN;
    gs["password"] = USER_PASSWORD;
    gs["sensor_id"] = (int32_t)SENSOR_ID;
    gs["sensor_data"] = temp;
    gs.endObj();
    gs.end();
    Serial.println(gs);

    post_data(gs, String(SERVER_IP) + String(MEASUREMENT_ENDPOINT));
}


void post_settings()
{
  gson::string gs;

    // Формирование JSON
    gs.beginObj();
    gs["username"] = USER_LOGIN;
    gs["password"] = USER_PASSWORD;
    gs["sensor_id"] = (int32_t)SENSOR_ID;
    gs["sensor_settings"] = TargetTemp;
    gs.endObj();
    gs.end();
    Serial.println(gs);

    post_data(gs, String(SERVER_IP) + String(SETTINGS_ENDPOINT)
              + String(SENSOR_ID)+"/");
}


void post_data(String json, String endpoint)
{
  int httpCode;

  if ((WiFi.status() == WL_CONNECTED)) 
  {
    Serial.println(WiFi.localIP());

    WiFiClient client;
    HTTPClient http;

    Serial.print("[HTTP] begin...\n");
    Serial.println(endpoint);
    http.begin(client, endpoint);  // HTTP
    http.addHeader("Content-Type", "application/json");

    Serial.print("[HTTP] POST...\n");

    httpCode = http.POST(json);

    if (httpCode > 0)
    {
      // HTTP header has been send and Server response header has been handled
      Serial.printf("[HTTP] POST... code: %d\n", httpCode);

      if (httpCode == HTTP_CODE_OK)
      {
        const String& payload = http.getString();
        Serial.println("received payload:\n<<");
        Serial.println(payload);
        Serial.println(">>");
      }
    } 
    else 
    {
      Serial.printf("[HTTP] POST... failed, error: %s\n", http.errorToString(httpCode).c_str());
    }

    http.end();
  }
}


void get_settings()
{
  int httpCode;
  gson::Parser parsed;

  if ((WiFi.status() == WL_CONNECTED))
  {
    Serial.println(WiFi.localIP());

    WiFiClient client;
    HTTPClient http;

    String endpoint = String(SERVER_IP) + String(SETTINGS_ENDPOINT+
                      String(SENSOR_ID)+"/");

    Serial.print("[HTTP] begin...\n");
    Serial.println(endpoint);
    http.begin(client, endpoint);  // HTTP
    http.addHeader("Content-Type", "application/json");
    http.addHeader("user-agent", "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36");

    Serial.print("[HTTP] GET...\n");

    httpCode = http.GET();
    if (httpCode > 0)
    {
      Serial.printf("[HTTP] GET... code: %d\n", httpCode);

      if (httpCode == HTTP_CODE_OK  || httpCode == HTTP_CODE_MOVED_PERMANENTLY)
      {
        String payload = http.getString();
        Serial.println("received payload:\n<<");
        Serial.println(payload);
        Serial.println(">>");

        parsed.parse(payload);
        if(parsed.hasError())
        {
          Serial.print(parsed.readError());
        }
        else
        {
          float new_value = parsed["setting"];
          Serial.println(new_value);
          Serial.println("OK read json");
          if(new_value!=TargetTemp)
          {
            TargetTemp = new_value;
            CheckAndSaveSettings();
            Serial.println("New settings saved");
          }
        }

      }
    }
    else
    {
      Serial.printf("[HTTP] GET... failed, error: %s\n", http.errorToString
      (httpCode).c_str());
    }
    http.end();
  }
}


void loop() 
{
  if(TimerTick==0) LED_ON;
  if(TimerTick==1) LED_OFF;


  eb.tick();

  if (eb.left())
  {
    if(CurrentMode == SHOW_TEMP)
    {
      if(Brightness!=0) 
      {
        Brightness--;
        CheckAndSaveSettings();
        ShowTemp(CurrentTemp);
      }
      Serial.print("Brightness = ");
      Serial.println(Brightness);
    }
  }

  if (eb.right())
  {
    if(CurrentMode == SHOW_TEMP)
    {
      if(Brightness!=7) 
      {
        Brightness++;
        CheckAndSaveSettings();
        ShowTemp(CurrentTemp);
      }
      Serial.print("Brightness = ");
      Serial.println(Brightness);
    }
  }


  if(eb.click() && CurrentMode == SHOW_TEMP)      // Вывод заданной температуры 
  {
    Serial.println("SHOW_TARGET_TEMP Mode");
    CurrentMode = SHOW_TARGET_TEMP;
    ShowTemp(TargetTemp);
    CustomTimerTicker=0;
    TempTimer=0;
  }
  if(CurrentMode==SHOW_TARGET_TEMP)
  {
    if(CustomTimerTicker==10)
    {
      CustomTimerTicker=0;
      TempTimer++;
      if(TempTimer==3)
      {
        Serial.println("SHOW_TEMP Mode");
        CurrentMode = SHOW_TEMP;
        TempTimer=0;
        ShowTemp(CurrentTemp);
      }
    }
  }


  if(eb.hold())    // Изменение целевой температуры
  {
    if(CurrentMode == SHOW_TEMP)
    {
      CurrentMode=ADJUST_TARGET_TEMP;
      Serial.println("ADJUST_TARGET_TEMP Mode");
    }
    else if(CurrentMode == ADJUST_TARGET_TEMP) 
    {
      CurrentMode = SHOW_TEMP;
      Serial.println("SHOW_TEMP Mode");
      ShowTemp(CurrentTemp);
      CheckAndSaveSettings();
      post_settings();
    }
  }

  if(CurrentMode == ADJUST_TARGET_TEMP)
  {
    if (eb.left())
    {
      Serial.println("ADJUST_TARGET_TEMP TargetTemp--");
      if(TargetTemp>MIN_SENSOR_VALUE)
      {
        TargetTemp = TargetTemp-0.1;
        ShowTemp(TargetTemp);
      }
    }
    if (eb.right())
    {
      Serial.println("ADJUST_TARGET_TEMP TargetTemp++");
      if(TargetTemp<MAX_SENSOR_VALUE)
      {
        TargetTemp = TargetTemp+0.1;
        ShowTemp(TargetTemp);
      }
    }
    if(isTicker==1)
    {
      if(LedTimerTicker==0 || LedTimerTicker==5)
      {
        isTicker=0;
        ShowTemp(TargetTemp);
      }
    }
  }


  if(ReadTempComplete==1)        // Вывод показаний датчика
  {
    ReadTempComplete=0;
    Serial.print("Current temp = ");
    Serial.println(TempFloat);
    if(CurrentMode == SHOW_TEMP)  ShowTemp(CurrentTemp);
  }

  if(http_timer >= SERVER_POST_MESSAGE_INTERVAL_x10ms
      && CurrentMode == SHOW_TEMP)    // Отправка данных на сервер
  {
    post_measurement(TempFloat);
    get_settings();
    http_timer=0;
  }
}
