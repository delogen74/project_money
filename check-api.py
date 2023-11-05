import requests

def check_api():
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    response = requests.get(url)
    data = response.json()  # Используем .json() для преобразования ответа в JSON

    print(data)

if __name__ == '__main__':
    check_api()
