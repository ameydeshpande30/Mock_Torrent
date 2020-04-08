from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import base64


pr_key = RSA.importKey(open('pub/private_pem.pem', 'r').read())
pb_key = RSA.importKey(open('pub/1111.pub', 'r').read())


cipher = PKCS1_OAEP.new(key=pb_key)


uid =b'209176'

# ct = cipher.encrypt(uid)
# ls = base64.b64encode(ct).decode()
# print(ls.encode())

ls = "qZiOietm6CvwRjgEqAL4uQgxnf1PsdR3KmRdHtmJDWpKcbtsdYdNTk+dst9WrQAhJafy2DAWbh0tdgAVV6BEiWG/fLRddO11JM0+JyKnqG75aqHFX4sXacH4UaoBStN3jHUoXoVzPuGCR8iWnLJ0Mob2lDUDcIoI+1iW606YZ9Q="
c2 = PKCS1_OAEP.new(key=pr_key)

uuu = base64.decodebytes(ls.encode())
print(uuu)
print(c2.decrypt(uuu))
