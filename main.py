import math

from services.degiro_service import DegiroService
from services.telegram_service import TelegramBotService
from dotenv import load_dotenv

INVESTMENT_RULES = [
    {
        # Vanguard S&P 500 VUAA
        # 'degiro_id': '16954338',

        # iShares Core MSCI World UCITS ETF (IWDA)
        'degiro_id': '846772',
        'percentage': 1,
    },
]

load_dotenv()

degiro = DegiroService()
telegram = TelegramBotService()

investable_amount = degiro.get_investable_amount() - 100  # €100 for fees etc

did_invest = False

for rule in INVESTMENT_RULES:
    product = degiro.get_product_details(rule['degiro_id'])

    amount = investable_amount * rule['percentage']

    qty = math.floor(amount / product['closePrice'])
    price = amount / qty

    if qty > 0:
        confirmation = degiro.place_order(rule['degiro_id'], qty, price)

        if confirmation:
            did_invest = True

            telegram.send_message_sync(
                f"""
                Invested €{round(qty * product['closePrice'], 2)} in {product['name']}.\n\nQuantity: {qty}\nProduct Price: €{product['closePrice']}
                """
            )
        else:
            telegram.send_message_sync(
                f"""
                There was an error when investing €{round(qty * product['closePrice'], 2)} in {product['name']}.\n\nQuantity: {qty}\nProduct price: €{product['closePrice']}
                """
            )

if not did_invest:
    telegram.send_message_sync(
        f"""
        Did not invest, something went wrong. You have an investable amount of €{round(investable_amount, 2)}.
        """
    )
