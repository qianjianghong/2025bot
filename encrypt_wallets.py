import json
from Crypto.Cipher import AES
import os

def encrypt_wallets(wallets_dict, secret_key, output_file="wallets.enc"):
    data = json.dumps(wallets_dict).encode("utf-8")
    cipher = AES.new(secret_key.encode("utf-8"), AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data)
    with open(output_file, "wb") as f:
        f.write(nonce + ciphertext)
    print(f"✅ 加密完成，输出文件: {output_file}")

if __name__ == "__main__":
    wallets = {
        "user_001": {
            "address": "4xMySolWallet111",
            "private_key": "privkey1111..."
        },
        "user_002": {
            "address": "5xYourSolWallet222",
            "private_key": "privkey2222..."
        }
    }
    secret_key = os.getenv("WALLET_SECRET_KEY", "1234567890abcdef")
    encrypt_wallets(wallets, secret_key)
