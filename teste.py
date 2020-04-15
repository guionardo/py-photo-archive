from photoinfo import Imagem

Imagem.setupDB('.')

img = Imagem("_20160817_092703.JPG")
print(img.UpdateDB())

print(img)