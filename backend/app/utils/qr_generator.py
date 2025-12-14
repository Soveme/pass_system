import qrcode
from io import BytesIO
import base64
from typing import Tuple

def generate_qr_code(data: str) -> Tuple[str, bytes]:
    """Generate QR code and return as base64 string and bytes"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to bytes
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_bytes = buffer.getvalue()
    
    # Convert to base64
    img_base64 = base64.b64encode(img_bytes).decode()
    
    return img_base64, img_bytes
