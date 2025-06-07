import math

from services.degiro_service import DegiroService
from services.telegram_service import TelegramBotService
from dotenv import load_dotenv

# Minimum investment amount to get transaction discount
MINIMUM_INVESTMENT = 1000

INVESTMENT_RULES = [
    {
        # iShares Core MSCI World UCITS ETF (IWDA)
        'degiro_id': '846772',
        'percentage': 1,
    },
]

load_dotenv()

degiro = DegiroService()
telegram = TelegramBotService()

investable_amount = degiro.get_investable_amount() - 1 # €1 for transaction fee

did_invest = False

for rule in INVESTMENT_RULES:
    product = degiro.get_product_details(rule['degiro_id'])
    share_price = product['closePrice']

    # Calculate minimum shares needed to reach €1000 investment
    min_qty_for_discount = math.ceil(MINIMUM_INVESTMENT / share_price)
    
    # Calculate how much we can actually invest
    max_qty_affordable = math.floor(investable_amount / share_price)
    
    # Choose the minimum quantity needed for discount, but don't exceed what we can afford
    if max_qty_affordable >= min_qty_for_discount:
        qty = min_qty_for_discount
        investment_amount = qty * share_price
        
        telegram.send_message_sync(
            f"📊 Investment calculation:\n"
            f"💰 Available: €{round(investable_amount, 2)}\n"
            f"📈 Share price: €{round(share_price, 2)}\n"
            f"🎯 Minimum for discount: €{MINIMUM_INVESTMENT}\n"
            f"📦 Shares needed: {min_qty_for_discount}\n"
            f"✅ Investing: €{round(investment_amount, 2)}"
        )
    else:
        # Not enough money for discount, invest maximum possible
        qty = max_qty_affordable
        investment_amount = qty * share_price
        
        telegram.send_message_sync(
            f"⚠️ Investment calculation:\n"
            f"💰 Available: €{round(investable_amount, 2)}\n"
            f"📈 Share price: €{round(share_price, 2)}\n"
            f"🎯 Need €{MINIMUM_INVESTMENT} for discount\n"
            f"❌ Can only afford {max_qty_affordable} shares\n"
            f"💸 Investing: €{round(investment_amount, 2)} (no discount)"
        )

    if qty > 0:
        confirmation = degiro.place_order(rule['degiro_id'], qty, share_price)

        if confirmation:
            did_invest = True

            telegram.send_message_sync(
                f"✅ Order placed successfully!\n"
                f"📦 Quantity: {qty} shares\n"
                f"💰 Total: €{round(investment_amount, 2)}\n"
                f"📈 Price per share: €{round(share_price, 2)}\n"
                f"🏢 Product: {product['name']}"
            )
        else:
            telegram.send_message_sync(
                f"❌ Order failed!\n"
                f"📦 Attempted: {qty} shares\n"
                f"💰 Amount: €{round(investment_amount, 2)}\n"
                f"📈 Price: €{round(share_price, 2)}\n"
                f"🏢 Product: {product['name']}"
            )

if not did_invest:
    telegram.send_message_sync(
        f"""
        Did not invest, something went wrong. You have an investable amount of €{round(investable_amount, 2)}.
        """
    )
