# thermo_sensors
Стек: Python, FastAPI, HTML, CSS, C, ESP8266
### Находится в разработке.
Управление и мониторинг температурных режимов террариумов с возможностью удалённого управления</br>

Настройка подключения ESP8266</br>
SERVER_IP - адрес API сервера</br>
SERVER_POST_MESSAGE_INTERVAL_x10ms - Интервал обмена данными с API сервера кратный 10us</br>
WIFI_SSID - SSID точки доступа WiFi</br>
WIFI_PASS - Пароль WiFi</br>
RELAY_PIN - Порт подключения реле нагревателя</br>
DIO_PIN  - Порт подключения TM1637 DIO</br>
CLK_PIN  - Порт подключения TM1637 CLK</br>
TEMP_SENSOR_PIN - Порт подключения DS18B20</br></br>

Пример конфигурации:</br>
#define SERVER_POST_MESSAGE_INTERVAL_x10ms 10*5</br>
#define SERVER_IP "http://domain_name.com/api/sensors/"</br>
#define WIFI_SSID "WiFi SSID"</br>
#define WIFI_PASS "WiFi Password"</br>
#define LED_PIN 16</br>
#define RELAY_PIN 0</br>
#define DIO_PIN 4</br>
#define CLK_PIN 5</br>
#define TEMP_SENSOR_PIN 2</br>
