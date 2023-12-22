# UniversityNavigator

## Описание
"UniversityNavigator" — это навигатор для студентов и преподавателей, который облегчает перемещение по кампусу университета. Этот инструмент позволяет быстро и эффективно строить маршруты внутри учебных зданий, предоставляя точные указания от выбранного кабинета до пункта назначения. Достаточно отправить в нашем телеграм-боте названия начального и конечного кабинетов, и "UniversityNavigator" мгновенно предложит оптимальный маршрут, сэкономив ваше время и избавив от стресса поиска нужного места.

## Технологии
Для функционирования нашего навигатора мы использовали программные решения и библиотеки:
- `networkx`: для обработки и анализа сложных графов маршрутов внутри зданий.
- `Pillow`: для работы с изображениями, включая карты этажей и планировки зданий.
- `aiogram`: для создания телеграм-бота, который обеспечивает интерактивное взаимодействие с пользователем.
- `pytesseract`: для распознавания текста на изображениях, что позволяет получать информацию о номере кабинета с фотографии.

## Начало работы

### Предварительные требования
Прежде всего, убедитесь, что у вас установлены все библиотеки из файла `requirements.txt`:

### Клонирование репозитория
Для начала работы с проектом сначала склонируйте репозиторий на свой компьютер. Откройте терминал и выполните следующую команду:

```bash
git clone https://github.com/Molochko1990/UniversityNavigator.git
```
После клонирования репозитория перейдите в каталог проекта:

```bash 
cd C:\...\UniversityNavigator
```

### Установка
Для установки необходимых библиотек выполните следующую команду:

```bash
pip install -r requirements.txt
```
### Конфигурация телеграм-бота
Перед запуском телеграм-бота, вам необходимо указать токен вашего бота. Откройте файл `telebot.py` и замените значение `TOKEN` на токен вашего телеграм-бота:
```bash
TOKEN = 'Your_token'
```

Замените `Your_token` на реальный токен, полученный от BotFather в Telegram.

### Запуск телеграм-бота
После настройки токена запустите бота, выполнив следующую команду:
```bash
python telebot.py
```