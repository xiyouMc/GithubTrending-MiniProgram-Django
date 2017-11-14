import base64
f = open('donate.jpeg','rb')
base64Str = base64.b64encode(f.read())
f.close()

print base64Str
