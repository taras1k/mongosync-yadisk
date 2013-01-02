from datetime import datetime
from wraper import YDaw
import os

'''
  Use token or user name and password
'''
DB_NAME = '[Your DB name]'
USER = ''
PWD = ''
TOKEN = '[Your token]'

#add some params to dump mongo DB if needed
os.system('mongodump --db %s' % DB_NAME)
os.system('tar cvzf dump.tgz dump')

file_name = str(datetime.utcnow()).replace(' ', '\\')

#api = YDaw(user=USER, pwd=PWD)
api = YDaw(token=TOKEN)

if api.get_folder_status(DB_NAME) == 404:
    api.create_folder(DB_NAME)

file_str = open('dump.tgz')
file_str = file_str.read()

api.sync_file(DB_NAME, file_name, file_str)
