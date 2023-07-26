import base64
import os
import uuid
from datetime import datetime
from decimal import Decimal
from io import BytesIO
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import qrcode
from django.utils import timezone
from PIL import Image

from bcwallet.settings import (
    BASE_DIR,
    BLOCKCHAIN_MINIMUM_DEPOSIT_MAP,
    BLOCKCHAIN_NETWORK_MAP,
    ENVIRONMENT_SETTING,
)


def handle_blockchain_network(blockchain):
    if ENVIRONMENT_SETTING == "production":
        return blockchain, BLOCKCHAIN_NETWORK_MAP[blockchain]["production"]
    return blockchain, BLOCKCHAIN_NETWORK_MAP[blockchain]["development"]


def handle_minimum_deposit_amount(symbol):
    if ENVIRONMENT_SETTING == "production":
        return BLOCKCHAIN_MINIMUM_DEPOSIT_MAP[symbol]
    return Decimal(BLOCKCHAIN_MINIMUM_DEPOSIT_MAP[symbol]) / 10


def handle_transaction_code(symbol, user_id, trx_type="DP", merchant_code=None):
    user_id = str(user_id).zfill(8)
    uniq = uuid.uuid4().hex[:6].upper()
    now = datetime.now().strftime("%Y%m%d%H%M%S")

    if not merchant_code:
        return f"{trx_type}{symbol}{user_id}-{now}-{uniq}"

    return f"{trx_type}{symbol}{merchant_code}{user_id}-{now}-{uniq}"


def generate_qrcode_with_logo(text, logo_path="/icons/default.png"):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=15,
        border=2,
    )
    qr.add_data(text)
    qr.make(fit=True)

    qr_image = qr.make_image().convert("RGB")

    # Load the logo from base64
    # logo_full_path = os.path.join(settings.BASE_DIR, logo_path)
    logo_full_path = os.path.join(BASE_DIR, logo_path[1:])
    logo_image = Image.open(logo_full_path)

    # Resize the logo to 20% of the QR code size
    qr_size = qr_image.size
    logo_size = (qr_size[0] // 5, qr_size[1] // 5)
    logo_image = logo_image.resize(logo_size, Image.Resampling.LANCZOS)

    # Calculate the position to overlay the logo
    logo_position = ((qr_size[0] - logo_size[0]) // 2, (qr_size[1] - logo_size[1]) // 2)

    # Paste the logo onto the QR code image
    qr_image.paste(logo_image, logo_position)

    # Create a BytesIO object to hold the final image data
    image_buffer = BytesIO()
    qr_image.save(image_buffer, format="PNG")
    image_buffer.seek(0)

    # Encode the image data as base64
    base64_image = base64.b64encode(image_buffer.read()).decode("utf-8")
    return f"data:image/png;base64,{base64_image}"


def handle_created_at(utc_time, unix=True):
    if unix:
        return int(utc_time.timestamp())
    return timezone.localtime(utc_time)


def handle_url_parameter(url, new_parems={}):
    parsed_url = urlparse(url)
    current_params = parse_qs(parsed_url.query)
    current_params.update(new_parems)
    updated_query_string = urlencode(current_params, doseq=True)

    updated_url = urlunparse(
        (
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            parsed_url.params,
            updated_query_string,
            parsed_url.fragment,
        )
    )

    return updated_url


def get_transaction_notif_url(trx, status=None):
    query = {
        "user_id": trx.user_id,
        "merchant_code": trx.merchant.code,
        "trx_status": status if status else trx.status,
        "trx_code": trx.code,
        "trx_created_at": handle_created_at(utc_time=trx.created_at),
        "trx_amount": trx.amount,
    }
    if trx.origin_code:
        query["origin_code"] = trx.origin_code

    if trx.callback_url:
        return handle_url_parameter(url=trx.callback_url, new_parems=query)

    return
