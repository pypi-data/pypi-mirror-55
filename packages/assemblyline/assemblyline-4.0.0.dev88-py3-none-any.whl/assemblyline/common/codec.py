import os
import tempfile

from cart import pack_stream, unpack_stream, is_cart
from assemblyline.common import identify

# noinspection PyBroadException
def decode_file(original_path, fileinfo):
    extracted_path = None
    al_meta = {}
    with open(original_path, 'rb') as original_file:
        if is_cart(original_file.read(256)):
            original_file.seek(0)

            extracted_fd, extracted_path = tempfile.mkstemp()
            extracted_file = os.fdopen(extracted_fd, 'wb')

            cart_extracted = False
            try:
                hdr, _ = unpack_stream(original_file, extracted_file)
                al_meta = hdr.get("al", {}).get("meta", {})
                cart_extracted = True

            except Exception:
                extracted_path = None
                al_meta = {}
                fileinfo['type'] = 'corrupted/cart'

            finally:
                extracted_file.close()

            if cart_extracted:
                fileinfo = identify.fileinfo(extracted_path)

    return extracted_path, fileinfo, al_meta


# noinspection PyUnusedLocal
def encode_file(input_path, name):
    _, output_path = tempfile.mkstemp()

    with open(output_path, 'wb') as oh:
        with open(input_path, 'rb') as ih:
            data = ih.read(64)
            if not is_cart(data):
                ih.seek(0)
                pack_stream(ih, oh, {"name": name})
                return output_path, f"{name}.cart"
            else:
                return input_path, name

