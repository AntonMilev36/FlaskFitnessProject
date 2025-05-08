import base64

from werkzeug.exceptions import BadRequest


def decode_photo(path, encoded_str):
    with open(path, "wb") as f:
        try:
            f.write(base64.b64decode(encoded_str.encode("utf-8")))
        except Exception as ex:
            raise BadRequest("Invalid photo encoding")


def decode_video(path, encoded_str):
    with open(path, "wb") as f:
        try:
            f.write(base64.b64decode(encoded_str.encode("utf-8")))
        except Exception as ex:
            raise BadRequest("Invalid video encoding")
