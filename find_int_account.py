import json
import logging
import os
from dotenv import load_dotenv

from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.credentials import build_credentials

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.DEBUG)

# Build credentials from environment variables
credentials_dict = {
    "username": os.environ.get("DEGIRO_USERNAME"),
    "password": os.environ.get("DEGIRO_PASSWORD"),
}

# Only add 2FA if it's provided
if os.environ.get("DEGIRO_2FA_SECRET_KEY"):
    credentials_dict["totp_secret_key"] = os.environ.get("DEGIRO_2FA_SECRET_KEY")

credentials = build_credentials(override=credentials_dict)

trading_api = TradingAPI(credentials=credentials)
trading_api.connect()

# FETCH CONFIG TABLE
client_details_table = trading_api.get_client_details()

# EXTRACT DATA
int_account = client_details_table["data"]["intAccount"]
user_token = client_details_table["data"]["id"]
client_details_pretty = json.dumps(
    client_details_table,
    sort_keys=True,
    indent=4,
)

# DISPLAY DATA
print("\n" + "="*50)
print('Your "int_account" is:', int_account)
print('Your "user_token" is:', user_token)
print("="*50)
print("\nAdd this to your .env file:")
print(f"DEGIRO_INT_ACCOUNT={int_account}")
print("="*50)