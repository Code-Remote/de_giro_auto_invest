import os
from datetime import date
from pprint import pprint

from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.account import UpdateOption, UpdateRequest
from degiro_connector.trading.models.order import HistoryRequest, Action, Order, OrderType, TimeType


class DegiroService:
    def __init__(self):
        self.credentials = Credentials(
            int_account=os.environ.get("DEGIRO_INT_ACCOUNT"),
            username=os.environ.get("DEGIRO_USERNAME"),
            password=os.environ.get("DEGIRO_PASSWORD"),
            totp_secret_key=os.environ.get("DEGIRO_2FA_SECRET_KEY"),
        )
        self.trading_api = TradingAPI(credentials=self.credentials)
        self.trading_api.connect()

    def get_investable_amount(self):
        res = self.trading_api.get_update(
            request_list=[
                UpdateRequest(
                    option=UpdateOption.TOTAL_PORTFOLIO,
                    last_updated=0,
                ),
            ],
            raw=True,
        )

        return [d for d in res['totalPortfolio']['value'] if d.get('name') == 'totalCash'][0]['value']

    def get_portfolio(self):
        return self.trading_api.get_update(
            request_list=[
                UpdateRequest(
                    option=UpdateOption.ALERTS,
                    last_updated=0,
                ),
                UpdateRequest(
                    option=UpdateOption.CASH_FUNDS,
                    last_updated=0,
                ),
                UpdateRequest(
                    option=UpdateOption.HISTORICAL_ORDERS,
                    last_updated=0,
                ),
                UpdateRequest(
                    option=UpdateOption.ORDERS,
                    last_updated=0,
                ),
                UpdateRequest(
                    option=UpdateOption.PORTFOLIO,
                    last_updated=0,
                ),
                UpdateRequest(
                    option=UpdateOption.TOTAL_PORTFOLIO,
                    last_updated=0,
                ),
                UpdateRequest(
                    option=UpdateOption.TRANSACTIONS,
                    last_updated=0,
                ),
            ],
            raw=True,
        )

    def get_client_details(self):
        return self.trading_api.get_client_details()

    def get_product_details(self, product_id):
        res = self.trading_api.get_products_info(
            product_list=[product_id],
            raw=True,
        )

        return res['data'][product_id]

    def get_products_config(self):
        return self.trading_api.get_products_config()

    def get_orders_history(self):
        return self.trading_api.get_orders_history(
            history_request=HistoryRequest(
                from_date=date(
                    year=date.today().year - 1,
                    month=date.today().month,
                    day=date.today().day
                ),
                to_date=date.today(),
            ),
            raw=False,
        )

    def get_transactions_history(self):
        return self.trading_api.get_transactions_history(
            transaction_request=HistoryRequest(
                from_date=date(
                    year=date.today().year - 1,
                    month=date.today().month,
                    day=date.today().day
                ),
                to_date=date.today(),
            ),
            raw=True,
        )

    def get_account_info(self):
        return self.trading_api.get_account_info()

    def get_favorites(self):
        return self.trading_api.get_favorite(raw=True)

    def place_order(self, product_id, size, price):
        order = Order(
            buy_sell=Action.BUY,
            order_type=OrderType.MARKET,
            # order_type=OrderType.LIMIT,
            # price=price,
            product_id=product_id,
            size=size,
        )

        checking_response = self.trading_api.check_order(order=order, raw=True)

        if checking_response:
            confirmation = self.trading_api.confirm_order(
                confirmation_id=checking_response['data']['confirmationId'],
                order=order,
            )

            return confirmation

        return False
