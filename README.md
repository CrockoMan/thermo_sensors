# Управление и мониторинг режима работы термоконтроллеров
Стек: Python, FastAPI, HTML, CSS, C, ESP8266
### Находится в разработке.
Проект предназначен для управление и мониторинг температурных режимов террариумов с возможностью удалённого управления. Подключение нескольких температурных контроллеров к API, с возможностью промотра и корректировки режима работы, возможность ручной корректировки режима работы энкодерами температурных контроллеров</br></br>

Реализовано esp8266 (C):</br>
Котнроль температурного режима термоконтроллерами</br>
Ручная регулировка температурного режима</br>
Подключение термоконтроллера к WiFi</br>
Сохранение настроек в энергонезависимой памяти контроллера</br>
Передача текущей температуры серверу мониторинга</br>
TODO:</br>
Получение от сервера новых значений для температурного контроллера</br>
</br>

Реализовано сервер мониторинга и управления (Python FastAPI):</br>
Порлучение списка зарегистрированных термоконтроллеров API</br>
Получение одного термоконтроллера API</br>
Удаление термоконтроллера API</br>
TODO:</br>
Фронтенд отображения режимов работы термоконтроллеров</br>
Фронтенд изменение режимов работы термоконтроллеров</br>
Статистика температурных режимов за период</br>
</br>

Будущие планы расширения проекта:</br>
Android приложение с функцией мониторинга и управления</br>
</br>

Настройка подключения ESP8266</br>
SERVER_IP - адрес API сервера</br>
SERVER_POST_MESSAGE_INTERVAL_x10ms - Интервал обмена данными с API сервера кратный 10us</br>
WIFI_SSID - SSID точки доступа WiFi</br>
WIFI_PASS - Пароль WiFi</br>
RELAY_PIN - Порт подключения реле нагревателя</br>
DIO_PIN  - Порт подключения TM1637 DIO</br>
CLK_PIN  - Порт подключения TM1637 CLK</br>
TEMP_SENSOR_PIN - Порт подключения DS18B20</br></br>

Пример конфигурации esp8266:</br>
#define SERVER_POST_MESSAGE_INTERVAL_x10ms 10*5</br>
#define SERVER_IP "http://domain_name.com/api/sensors/"</br>
#define WIFI_SSID "WiFi SSID"</br>
#define WIFI_PASS "WiFi Password"</br>
#define LED_PIN 16</br>
#define RELAY_PIN 0</br>
#define DIO_PIN 4</br>
#define CLK_PIN 5</br>
#define TEMP_SENSOR_PIN 2</br></br>


Документация API backend доступна по адресу: http://domain_name/docs</br>

Автор: К.Гурашкин
