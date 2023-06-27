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
    'bitcoin'               : '/media/icons/btc.png',
    'bitcoin-cash'          : '/media/icons/bitcoin-cash.png',
    'litecoin'              : '/media/icons/litecoin.png',
    'dogecoin'              : '/media/icons/dogecoin.png',
    'dash'                  : '/media/icons/dash.png',
    'ethereum'              : '/media/icons/ethereum.png',
    'ethereum-classic'      : '/media/icons/etherum-classic.png',
    'xrp'                   : '/media/icons/xrp.png',
    'zcash'                 : '/media/icons/zcash.png',
    'binance-smart-chain'   : '/media/icons/binance-smart-chain.png',
    'tron'                  : '/media/icons/tron.png'
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
        'production': 'mainnet'
    }
}