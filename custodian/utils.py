import hashlib
import hmac
import base64


def get_service_token():
    domain = 'AGENT'
    secret = 'b1b4a229c0cb5865f67f0626dc9c184526dc6dd99f8f505b14d1c95739d523dfcfaa17534ea160364fe27e10e6c331a1c231f60be581e69fed4f5bf9c4dfdadb'
    key = hashlib.sha1(b'trood.signer' + secret.encode('utf-8')).digest()
    signature = hmac.new(key, msg=domain.encode('utf-8'), digestmod=hashlib.sha1).digest()
    signature = base64.urlsafe_b64encode(signature).strip(b'=')
    return 'Service {}:{}'.format(domain, signature.decode("utf-8"))
