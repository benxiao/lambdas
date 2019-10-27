import base64


def image_bytes_to_b64string(content: bytes) -> str:
    return base64.b64encode(content).decode("utf-8")


def b64string_to_image_bytes(content: str) -> bytes:
    return base64.b64decode(content.encode("utf-8"))


def encode_base64string_from(fn: str):
    with open(fn, 'rb') as fp:
        result = image_bytes_to_b64string(fp.read())
        print(type(result))
        return result


def decode_base64string_to(content: str, fn):
    with open(fn, "wb") as fp:
        fp.write(base64.b64decode(content.encode('utf-8')))
