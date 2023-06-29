STATUS_OPTIONS = (
    'active', 'Active',
    'nonactive', 'Nonactive'
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
    'bitcoin'               : '/storages/icons/btc.png',
    'bitcoin-cash'          : '/storages/icons/bitcoin-cash.png',
    'litecoin'              : '/storages/icons/litecoin.png',
    'dogecoin'              : '/storages/icons/dogecoin.png',
    'dash'                  : '/storages/icons/dash.png',
    'ethereum'              : '/storages/icons/ethereum.png',
    'ethereum-classic'      : '/storages/icons/etherum-classic.png',
    'xrp'                   : '/storages/icons/xrp.png',
    'zcash'                 : '/storages/icons/zcash.png',
    'binance-smart-chain'   : '/storages/icons/binance-smart-chain.png',
    'tron'                  : '/storages/icons/tron.png'
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
    'bitcoin' : '0.0001',
    'bitcoin-cash' : '0.01',
    'litecoin' : '0.01',
    'dogecoin' : '20.00',
    'dash' : '0.1',
    'ethereum' : '0.001',
    'ethereum-classic' : '0.1',
    'xrp' : '4.00',
    'zcash' : '0.1',
    'binance-smart-chain' : '0.01',
    'tron' : '0.01',
}