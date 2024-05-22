import ssl
import tempfile


def create_ssl_context(cert_str: str, key_str: str) -> ssl.SSLContext:
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE

    cert_file = get_filled_file(cert_str.replace('\\n', '\n').encode())
    key_file = get_filled_file(key_str.replace('\\n', '\n').encode())

    ssl_ctx.load_cert_chain(
        certfile=cert_file.name,
        keyfile=key_file.name
    )

    return ssl_ctx


def get_filled_file(data: bytes) -> tempfile.NamedTemporaryFile:
    file = tempfile.NamedTemporaryFile()
    file.write(data)
    file.seek(0)

    return file
