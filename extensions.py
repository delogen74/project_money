import requests
from config import API_TOKEN


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def convert_to_rub(amount, currency):
        """Конвертирует указанную сумму в рубли."""
        response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
        response.raise_for_status()
        data = response.json()['Valute']
        if currency in data:
            rate = data[currency]['Value'] / data[currency]['Nominal']
            return amount * rate
        elif currency == 'RUB':
            return amount
        else:
            raise APIException(f"Валюта {currency} не найдена.")

    @staticmethod
    def get_price(base, quote, amount):
        if base == quote:
            raise APIException("Валюты не должны совпадать.")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException("Неверное количество валюты.")

        try:
            rub_amount = CurrencyConverter.convert_to_rub(amount, base)
            if quote == 'RUB':
                return f"Сумма в {amount} {base} составляет {rub_amount:.2f} {quote}"
            else:
                # Переводим из рублей в целевую валюту
                rub_to_quote_amount = CurrencyConverter.convert_to_rub(1, quote)
                converted_price = rub_amount / rub_to_quote_amount
                return f"Сумма в {amount} {base} составляет {converted_price:.2f} {quote}"
        except APIException as e:
            raise
        except Exception as e:
            raise APIException(f"Произошла ошибка при получении данных о курсе валют: {e}")

