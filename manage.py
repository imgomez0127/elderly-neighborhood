from settings import app
import views
from settings import bcrypt
if __name__ == '__main__':
	
	app.run(host = "0.0.0.0",debug = True)