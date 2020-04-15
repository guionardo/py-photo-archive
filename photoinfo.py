import datetime
import hashlib
import os

from exif import Image
from persistence import ImageRecord
from sqlite_orm.database import Database


class Imagem:

    dbpath = None

    def __init__(self, arquivo: str):
        if not (os.path.exists(arquivo) and os.path.isfile(arquivo)):
            raise FileNotFoundError(arquivo)

        self.arquivo = arquivo
        dt_exif = None
        with open(arquivo, 'rb') as img:
            e = Image(img)

            if e.has_exif:
                for td in ['datetime', 'datetime_digitized', 'datetime_original']:
                    dt_exif = e.get(td)
                    if dt_exif is not None:
                        break
        dt_file = datetime.datetime.fromtimestamp(os.path.getmtime(arquivo))
        if dt_exif is None:
            dt_exif = dt_file
        else:
            dt_exif = datetime.datetime.strptime(dt_exif, '%Y:%m:%d %H:%M:%S')

        self.datetime_exif = dt_exif
        self.datetime_file = dt_file

        hasher = hashlib.md5()
        with open(arquivo, 'rb') as afile:
            buf = afile.read()
            hasher.update(buf)

        self.md5 = hasher.hexdigest()

    def __str__(self):
        return "{}:{}:{}:{}".format(self.arquivo, self.datetime_exif, self.datetime_file, self.md5)

    
    @staticmethod
    def setupDB(dbpath:str):
        if os.path.isdir(dbpath):
            dbpath = os.path.join(dbpath,'photoinfo.db')
        
        Imagem.dbpath = dbpath

    def UpdateDB(self):
        if Imagem.dbpath==None:
            return False
        with Database(Imagem.dbpath) as db:
            db.query(ImageRecord).create().execute()
            imagem = ImageRecord(id=self.md5,name=self.arquivo)
            found = False
            for row in db.query(ImageRecord,self.md5).select().execute():
                found = True
                break
            if not found:
                db.query().insert(imagem).execute()
            else:                
                db.query(ImageRecord).update()
