import telebot
import requests
from config import API_TOKEN
from extensions import CurrencyConverter, APIException

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    instructions = """
    Для получения курса валюты используйте команду в следующем формате:
    <имя валюты, цену которой вы хотите узнать> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>

    Например: USD RUB 100

    Для получения списка доступных валют используйте команду /values.
    """
    bot.send_message(message.chat.id, instructions)

@bot.message_handler(commands=['values'])
def handle_values(message):
    try:
        response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
        response.raise_for_status()
        currency_data = response.json()['Valute']
        available_currencies = "Доступные валюты:\n" + "\n".join([f"{currency} - {info['Name']}" for currency, info in currency_data.items()])
        bot.send_message(message.chat.id, available_currencies)
    except requests.RequestException as e:
        bot.send_message(message.chat.id, f"Не удалось получить данные с сервера: {e}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    try:
        base, quote, amount = message.text.split()
        price = CurrencyConverter.get_price(base, quote, amount)
        bot.send_message(message.chat.id, price)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите команду в правильном формате.")
    except APIException as e:
        bot.send_message(message.chat.id, str(e))
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")

if __name__ == '__main__':
    bot.polling(none_stop=True)
