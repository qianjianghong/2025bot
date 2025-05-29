import json
from Crypto.Cipher import AES

def decrypt_wallet_config(enc_file, secret_key):
    with open(enc_file, "rb") as f:
        data = f.read()
    nonce, ciphertext = data[:16], data[16:]
    cipher = AES.new(secret_key.encode("utf-8"), AES.MODE_EAX, nonce=nonce)
    decrypted = cipher.decrypt(ciphertext)
    return json.loads(decrypted.decode("utf-8"))

if __name__ == "__main__":
    secret_key = input("请输入16位解密密钥: ")
    wallets = decrypt_wallet_config("wallets.enc", secret_key)
    print("✅ 解密成功，钱包数据如下：")
    print(json.dumps(wallets, indent=2))
