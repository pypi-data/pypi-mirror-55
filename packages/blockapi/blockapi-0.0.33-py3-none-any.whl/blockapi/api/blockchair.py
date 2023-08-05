from datetime import datetime

import dateutil.parser
import pytz

from blockapi.services import (
    BlockchainAPI,
    set_default_args_values,
    AddressNotExist
)


class BlockchairAPI(BlockchainAPI):
    """
    Multi coins: bitcoin, bitcoin-cash, bitcoin-sv, litecoin, dogecoin, dash,
                 ethereum, groestlcoin
    API docs: https://github.com/Blockchair/Blockchair.Support/blob/master/API_DOCUMENTATION_EN.md
    Explorer: https://blockchair.com
    """

    active = False

    symbol = None
    rate_limit = 0
    coef = None
    start_offset = 0
    max_items_per_page = 10  # 10000 per tx hashes; 10 per tx details
    page_offset_step = max_items_per_page
    xpub_support = True

    supported_requests = {
        # for limit and offset the second parameter 0 is for utxo
        'get_dashboard': '/{symbol}/dashboards/{address_type}/{address}?limit={limit},0&offset={offset},0',
        'get_txs': '/{symbol}/dashboards/transactions/{hash_or_hashes}',
    }

    def __init__(self, address, api_key=None):
        super().__init__(address, api_key)
        self._set_address_type()

    def _set_address_type(self):
        is_xpub = (any(self.address.startswith(p)
                       for p in ['xpub', 'ypub', 'zpub']))
        self.address_type = 'xpub' if is_xpub else 'address'

    def get_balance(self):
        dashboard = self._get_dashboard()
        if not dashboard:
            return 0

        # return dashboard[self.address_type]['balance'] * self.coef
        return int(dashboard['address']['balance']) * self.coef

    def get_create_date(self):
        dashboard = self._get_dashboard()
        if not dashboard:
            return 0

        date_str = dashboard[self.address_type]['first_seen_receiving']
        date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        return date.replace(tzinfo=pytz.UTC)

    @set_default_args_values
    def get_txs(self, offset=None, limit=None, unconfirmed=False):
        dashboard = self._get_dashboard(offset, limit)
        if not dashboard:
            return []

        tx_hashes = dashboard['transactions']
        tx_response = self.request(
            'get_txs',
            symbol=self.symbol,
            hash_or_hashes=','.join(tx_hashes)
        )
        if not tx_response.get('data'):
            return []

        txs = list(tx_response['data'].values())
        return [self.parse_tx(t) for t in txs]

    def parse_tx(self, tx):
        my_input = next((i for i in tx['inputs']
                         if self.address == i['recipient']), None)
        my_output = next((o for o in tx['outputs']
                          if self.address == o['recipient']), None)
        tx_data = tx['transaction']

        if my_input:
            amount = my_input['value'] * self.coef
            direction = 'outgoing'
            from_address = self.address
            to_address = (tx['outputs'][0]['recipient']
                          if tx_data['output_count'] == 1 else 'multiple')
        else:
            amount = my_output['value'] * self.coef
            direction = 'incoming'
            to_address = self.address
            from_address = (tx['inputs'][0]['recipient']
                            if tx_data['input_count'] == 1 else 'multiple')

        return {
            'date': dateutil.parser.parse(tx_data['time']),
            'from_address': from_address,
            'to_address': to_address,
            'amount': amount,
            'fee': tx_data['fee'] * self.coef,
            'gas': {},
            'hash': tx_data['hash'],
            'confirmed': None,
            'is_error': False,
            'type': 'normal',
            'kind': 'transaction',
            'direction': direction,
            'raw': tx
        }

    def _get_dashboard(self, offset=0, limit=0):
        response = self.request(
            'get_dashboard',
            symbol=self.symbol,
            address_type=self.address_type,
            address=self.address,
            offset=offset,
            limit=limit
        )

        data = response.get('data')
        if not data:
            raise AddressNotExist()

        dashboard = list(data.values())[0]

        if self.address_type == 'address':
            if not dashboard['address']['type']:
                raise AddressNotExist()

        return dashboard


class BlockchairBitcoinAPI(BlockchairAPI):
    symbol = 'BTC'
    coef = 1e-8


class BlockchairBitcoinCashAPI(BlockchairAPI):
    symbol = 'BCH'
    coef = 1e-8


class BlockchairBitcoinSvAPI(BlockchairAPI):
    symbol = 'BSV'
    # coef = 1e-8


class BlockchairLitecoinAPI(BlockchairAPI):
    symbol = 'LTC'
    coef = 1e-8


class BlockchairDogecoinAPI(BlockchairAPI):
    symbol = 'DOGE'
    coef = 1e-8


class BlockchairDashAPI(BlockchairAPI):
    symbol = 'DASH'
    coef = 1e-8


class BlockchairEthereumAPI(BlockchairAPI):
    symbol = 'ETH'
    coef = 1e-18


class BlockchairGroestlcoinAPI(BlockchairAPI):
    symbol = 'GRS'
    coef = 1e-8

# class BlockchairRippleAPI(BlockchairAPI):
#     symbol = 'XRP'
#     coef = 1e-8
