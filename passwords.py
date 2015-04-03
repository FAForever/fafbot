from PySide.QtSql import QSqlQuery
import rsa, base64
import traceback
from Crypto.Cipher import AES
import re
import json
import hashlib

PRIVATE_KEY = rsa.PrivateKey.load_pkcs1(base64.b64decode("MIGUAgEAAhwOCYK+a8WeokqSHqKhGLVMzfUF2tZdoeaW5DQnAgMBAAECHAH3aR5+AJBJkgLIUeYZfDKJBJGpb4iz/7mcuTECDj9GSDulHRiO//X1vSDvAg44ythldPwOVNJjzMcwSQIOE6UDahkyNly3VSqtRFsCDgC5rnvVO6bfNHSr19tpAg4UouL3z6gxb03hUN0FDg=="), format='DER')
DB_SERVER = "localhost"
DB_PORT = 3306
DB_LOGIN = "faf-server"
DB_PASSWORD = "Bi+pLur5of3Db5WfCqU9ocGWgcquzz+WD1lFNZMRZME=" 
DB_TABLE = "faf_lobby"

CHALLONGE_KEY = ""
CHALLONGE_USER = ""

PW_SALT = '(+3%_'

STEAM_APIKEY = "DE55A443A7049F76427314824024192C"
STEAM_FA_ID = 9420
 
MAIL_ADDRESS = "admin@forever.com"
MAIL_PASSWORD = ""

def decodeUniqueId(lobby, string, login):
    pass
