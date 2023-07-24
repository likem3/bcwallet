STATUS_OPTIONS_SERIALIZER = (
    'active', 'Active',
    'nonactive', 'Nonactive'
)

STATUS_CHOICES_MODEL = (
    ("active", "Active"),
    ("nonactive", "Non-active"),
    ("suspended", "Suspended"),
)

BLOCKCHAIN_OPTIONS = (
    ('bitcoin', 'BTC'),
    ('bitcoin-cash', 'BCH'),
    ('litecoin', 'LTC'),
    ('dogecoin', 'DOGE'),
    ('dash', 'DASH'),
    ('ethereum', 'ETH'),
    ('ethereum-classic', 'ETC'),
    ('xrp', 'XRP'),
    ('zcash', 'Zcash'),
    ('binance-smart-chain', 'BSC'),
    ('tron', 'TRON')
)

NETWORK_OPTIONS = (
    ('mainnet', 'Mainnet'),
    ('testnet', 'Testnet'),
    ('mordor', 'Mordor'),
    ('nile', 'Nile'),
    ('goerli', 'Goerli'),
)

LOGO_SETTINGS = {
    'BTC' : '/storages/icons/btc.png',
    'BCH' : '/storages/icons/bitcoin-cash.png',
    'LTC' : '/storages/icons/litecoin.png',
    'DOGE' : '/storages/icons/dogecoin.png',
    'DASH' : '/storages/icons/dash.png',
    'ETH' : '/storages/icons/ethereum.png',
    'ETC' : '/storages/icons/etherum-classic.png',
    'XRP' : '/storages/icons/xrp.png',
    'ZEC' : '/storages/icons/zcash.png',
    'BNB' : '/storages/icons/binance-smart-chain.png',
    'TRX' : '/storages/icons/tron.png',
    'USDT' : '/storages/icons/usdt.png',
}

BLOCKCHAIN_CODE = {
    'bitcoin'               : 'BTC',
    'bitcoin-cash'          : 'BCH',
    'litecoin'              : 'LTC',
    'dogecoin'              : 'DOGE',
    'dash'                  : 'DASH',
    'ethereum'              : 'ETH',
    'ethereum-classic'      : 'ETC',
    'xrp'                   : 'XRP',
    'zcash'                 : 'ZEC',
    'binance-smart-chain'   : 'BNB',
    'tron'                  : 'TRX'
}

NETWORK_CODE = {
    'testnet'   : 'TNT',
    'mainnet'   : 'MNT',
    'mordor'    : 'MRD',
    'nile'      : 'NLE',
    'goerli'    : 'GOE'
}

BLOCKCHAIN_NETWORK_MAP = {
    'bitcoin': {
        'production': 'mainnet',
        'development': 'testnet'
    },               
    'bitcoin-cash' : {
        'production': 'mainnet',
        'development': 'testnet'
    },
    'litecoin' : {
        'production': 'mainnet',
        'development': 'testnet'
    },
    'dogecoin' : {
        'production': 'mainnet',
        'development': 'testnet'
    },
    'dash' : {
        'production': 'mainnet',
        'development': 'testnet'
    },
    'ethereum' : {
        'production': 'mainnet',
        'development': 'goerli'
    },
    'ethereum-classic' : {
        'production': 'mainnet',
        'development': 'mordor'
    },
    'xrp' : {
        'production': 'mainnet',
        'development': 'testnet'
    },
    'zcash' : {
        'production': 'mainnet',
        'development': 'testnet'
    },
    'binance-smart-chain' : {
        'production': 'mainnet',
        'development': 'testnet'
    },
    'tron' : {
        'production': 'mainnet',
        'development': 'nile'
    },
}

BLOCKCHAIN_MINIMUM_DEPOSIT_MAP = {
    'BTC' : '0.0001',
    'BCH' : '0.01',
    'LTC' : '0.01',
    'DOGE' : '20.00',
    'DASH' : '0.1',
    'ETH' : '0.001',
    'ETC' : '0.1',
    'XRP' : '4.00',
    'ZEC' : '0.1',
    'BNB' : '0.01',
    'TRX' : '0.01',
    'USDT' : '0.001',
}

TRANSACTION_STATUS = (
    ("pending", "Pending"),
    ("confirming", "Confirming"),
    ("completed", "Completed"),
    ("failed", "Failed"),
    ("cancelled", "Cancelled"),
)

TRANSACTION_TYPE_OPTION = (
    ('deposit', "Deposit"),
    ('withdrawal', "Withdrawal"),
)

WALLET_TASK_STATUS = (
    ('open', 'Open'),
    ('success', 'Success'),
    ('fail', 'Fail'),
    ('cencel', 'Cancel'),
)

NETWORK_RULE = """
Network rule:
In a production env network value "mainnet" for all blockchain.
Else, "ethereum" use "goerli", "ethereum-classic" use "mordor",
"tron" use "nile", rest use "testnet".
"""

HELPER_TEXT = {
    "account_uuid": "Unique UUID of the registered user",
    "account_user_id": "User ID of the registered user",
    "account_email": "Email of the registered user",
    "account_username": "Username of the registered user",
    "user_id": "ID of the associated user (source: account.user_id)",
    "currency_id": "Related blockchain that will be used",
    "currency_name": "Related currency name used",
    "currency_symbol": "Related currency symbol used",
    "currency_blockchain": "Related currency blockchain used",
    "currency_std": "Related currency blockchain standard used",
    "currency_network": "Network of the wallet currency",
    "blockchain": "Related blockchain that will be used",
    "network": f"Blockchain network \n{NETWORK_RULE}",
    "account": "Related account object",
    "wallet": "Related wallet object",
    "address": "String address of the blockchain wallet",
    "wallet_label": "Label of the wallet",
    "address_qr": "Base64 representation of the wallet address",
    "wallet_symbol": "Wallet blockchain symbol (e.g., ETH, BTC, etc.)",
    "wallet_logo": "URL path to the wallet blockchain logo",
    "wallet_balance_amount": "Nominal amount in the wallet",
    "wallet_balance_unit": "Symbol of the wallet currency",
    "created_timestamp": "Timestamp of when the remote wallet was created",
    "trx_code": "Code of the transaction, also serves as the transaction identifier",
    "trx_origin_code": "Origin transaction if the transaction is derived from another transaction",
    "trx_from_address": "Currency address that sends in the transaction",
    "trx_to_address": "Currency address that receives in the transaction",
    "trx_from_currency": "Symbol of the source currency such as BTC, ETH, etc",
    "trx_to_currency": "Symbol of the target currency such as BTC, ETH, etc",
    "trx_from_address": "Currency address that sends in the transaction",
    "trx_amount": "Separated by a dot, the amount to be received (e.g., 0.001)",
    "trx_rate": "Separated by a dot, exchange rate if different currencies",
    "trx_status": "Transaction status",
    "trx_cancel_reason": "Reason why the transaction becomes canceled",
    "trx_proof_of_payment": "Image in base64 format of the transaction receipt",
    "trx_expired_at": "The expiration of the transaction before it gets ignored",
    "trx_transaction_id": "The transaction hash (txid)",
    "trx_type": "The transaction type",
    "wtt_transaction_code": "Transaction code related",
    "wtt_wallet_id": "Wallet id related",
    "wtt_attemp": "Number of attemp running task",
    "wtt_status": "Status task",
    "merchant": "merchant of the system",
    "merchant_code": "Merchant code identifier",
    "merchant_name": "Merchant name",
    "merchant_status": "Merchant status",
}