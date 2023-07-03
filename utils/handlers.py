import qrcode
import base64
import os
from io import BytesIO
import time
from PIL import Image
from bcwallet.settings import (
    BASE_DIR,
    BLOCKCHAIN_NETWORK_MAP,
    ENVIRONMENT_SETTING,
    NETWORK_CODE,
    BLOCKCHAIN_CODE,
    BLOCKCHAIN_MINIMUM_DEPOSIT_MAP,
)
from decimal import Decimal


def handle_blockchain_network(blockchain):
    if ENVIRONMENT_SETTING == "production":
        return blockchain, BLOCKCHAIN_NETWORK_MAP[blockchain]["production"]
    return blockchain, BLOCKCHAIN_NETWORK_MAP[blockchain]["development"]


def handle_minimum_deposit_amount(blockchain):
    if ENVIRONMENT_SETTING == "production":
        return BLOCKCHAIN_MINIMUM_DEPOSIT_MAP[blockchain]
    return Decimal(BLOCKCHAIN_MINIMUM_DEPOSIT_MAP[blockchain]) / 10


def handle_transaction_code(blockchain, network, user_id, transaction_type="DP"):
    user_id = str(user_id).zfill(8)
    ncode = NETWORK_CODE[network]
    bcode = BLOCKCHAIN_CODE[blockchain]
    return f"{transaction_type}{bcode}{ncode}-{user_id}-{int(time.time())}"


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
    logo_image = logo_image.resize(logo_size, Image.ANTIALIAS)

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
