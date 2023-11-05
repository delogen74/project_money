import requests
import json  # Импортируем модуль json

# Функция для получения данных о курсах валют с API Центрального Банка РФ
def get_currency_rates():
    response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Функция для обновления файла с курсами валют
def update_currency_file(currency_data):
    if currency_data:
        with open('currency_rates.json', 'w', encoding='utf-8') as file:
            json.dump(currency_data, file, ensure_ascii=False, indent=4)
        print("Currency rates have been updated.")
    else:
        print("No data to update.")

# Получаем данные о курсах валют
data = get_currency_rates()

# Обновляем файл с курсами валют
update_currency_file(data)
