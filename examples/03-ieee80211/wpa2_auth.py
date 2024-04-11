from hashlib import pbkdf2_hmac, sha1
import hmac
import hashlib

def to_bytes(num):
    return hex(num)[2:].encode("ascii")

def calculate_ptk(PMK, AA, SPA, ANonce, SNonce):
    MIN_AA_SPA = min(AA, SPA)
    MAX_AA_SPA = max(AA, SPA)
    MIN_ANonce_SNonce = min(ANonce, SNonce)
    MAX_ANonce_SNonce = max(ANonce, SNonce)

    PTK = b''
    for i in range(4):  # Iterate to generate 512 bits
        PTK += hmac.new(PMK, b"Pairwise key expansion" + b'\x00' + MIN_AA_SPA + MAX_AA_SPA + MIN_ANonce_SNonce + MAX_ANonce_SNonce + bytes([i]), hashlib.sha1).digest()

    # return PRF(PMK, b"Pairwise key expansion", MIN_AA_SPA + MAX_AA_SPA + MIN_ANonce_SNonce + MAX_ANonce_SNonce)
    return PTK[:64]

    
PSK = "Test1234!"
SSID = "examplenet"
PMK = pbkdf2_hmac('sha1', PSK.encode('ascii'), SSID.encode('ascii'), 4096, 32)
print("PMK")
print(PMK.hex())

AA = bytes.fromhex("1c:ed:6f:b2:70:bd".replace(":", ""))
SPA = bytes.fromhex("2c:db:07:40:9a:16".replace(":", ""))
ANonce = bytes.fromhex("3a4b19d360e946ffc039f98a811599ccb916631f7866f08f413caad6f240bd3b")
SNonce = bytes.fromhex("f5ea43a088b5593425e5d93cfc5c0a8aef627d978ee72dc16545d63e6d7522d6")

print("PTK")
print(calculate_ptk(PMK, AA, SPA, ANonce, SNonce).hex())