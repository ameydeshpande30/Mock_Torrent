# from Crypto.Cipher import PKCS1_OAEP
# from Crypto.PublicKey import RSA
# import base64

# import jwt
# pr_key = RSA.importKey(open('pub/private_pem.pem', 'r').read())
# pb_key = RSA.importKey(open('pub/1111.pub', 'r').read())


# cipher = PKCS1_OAEP.new(key=pb_key)


# uid =b'209176'

# # ct = cipher.encrypt(uid)
# # ls = base64.b64encode(ct).decode()
# # print(ls.encode())

# ls = "qZiOietm6CvwRjgEqAL4uQgxnf1PsdR3KmRdHtmJDWpKcbtsdYdNTk+dst9WrQAhJafy2DAWbh0tdgAVV6BEiWG/fLRddO11JM0+JyKnqG75aqHFX4sXacH4UaoBStN3jHUoXoVzPuGCR8iWnLJ0Mob2lDUDcIoI+1iW606YZ9Q="
# c2 = PKCS1_OAEP.new(key=pr_key)

# uuu = base64.decodebytes(ls.encode())
# print(uuu)
# print(c2.decrypt(uuu))


from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import base64
def getNumber(private_key_path, ciperText):
    cp = base64.decodebytes(ciperText.encode())
    pr_key = RSA.importKey(open(private_key_path, 'r').read())
    de = PKCS1_OAEP.new(key=pr_key)
    return de.decrypt(cp)


print(getNumber("pub/private_pem.pem", "d2fuIsy3nmT7uQxjAfIszxOMkV7LBi6X0mChPVCnD/8jT0z1Gl8w2ZXKxdleC84dpRHh+FF6QOTTuu4AKJiNp7+SBWjhZ3uzCWEKr6Tjsowg2UiVhmowZFFvNIzLkEKNEagb0VR099A2N3lHRgjZ26QBGHfjHBiflfaNmK9MgUk="))

import jwt
def jwtVerify(token):
    public_key = open('pub/JWT.pub').read()
    payload = jwt.decode(token, public_key, algorithms=['RS256'])
    return payload
   

print(jwtVerify("eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MDYzNzAzMTksInVzZXJfaWQiOiIxMTExIn0.U3ZEAU4bzZrjzqtItbcWIWohsoQ51JVAPo7P90Odb4nwX_1DX7psJiUMFD5qwvKAwwSMtD57D7gH1A7lEyX33Ee_IUh8Jmm3xci5g3T3xu39kG2PmmhpaZo9RLcbFWwCGpBzEPH7fX4ys0M0JmY4FaSfmwppeDwO2BsYM3T_xQU"))