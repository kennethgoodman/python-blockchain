import ecdsa
import base64

"""

Copied code from: SimpleCoin (github)

"""

def sign_ECDSA_msg(private_key, msg, curve=ecdsa.SECP256k1):
    """Sign the message to be sent
    private_key: must be hex
    msg: must have encode method

    return signature: base64 (to make it shorter)
    """
    bmessage = msg.encode()
    sk = ecdsa.SigningKey.from_string(bytes.fromhex(private_key), curve=curve)
    signature = base64.b64encode(sk.sign(bmessage))
    return signature, message

def genereate_ECDSA_sk(curve=ecdsa.SECP256k1):
	# TODO: genereate randomness
	return ecdsa.SigningKey.generate(curve=curve) 

def format_sk(sk):
	return sk.to_string().hex() 

def get_pub_key_from_sk(sk, sk_already_formatted=True):
	if not sk_already_formatted:
		sk = format_sk(sk)
	vk = sk.get_verifying_key() 
    return vk.to_string().hex()

def get_address_from_pub_key(public_key):
	return base64.b64encode(bytes.fromhex(public_key))

def generate_ECDSA_keys(curve=ecdsa.SECP256k1):
    """This function takes care of creating your private and public (your address) keys.
    It's very important you don't lose any of them or those wallets will be lost
    forever. If someone else get access to your private key, you risk losing your coins.

    private_key: str
    public_ley: base64 (to make it shorter)
    """
    sk = genereate_ECDSA_sk(curve=curve)
    vk = get_pub_key_from_sk(sk, sk_already_formatted=False)
    pk = vk.to_string().hex()
    addr = get_address_from_pub_key(pk)
    return sk, vk, pk, addr

def check_signature(signature, vk, msg):
    return vk.verify(signature, msg)