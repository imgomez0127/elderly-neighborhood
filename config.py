import os
home_dir = os.path.dirname(__file__).replace('\\', '/').replace('D:/','')
database_path = home_dir+"/db/oldppl.db"
class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////'+database_path
    SQLALCHEMY_TRACK_MODIFICATIONS = False
if __name__ == '__main__':
	print(Config.SQLALCHEMY_DATABASE_URI)