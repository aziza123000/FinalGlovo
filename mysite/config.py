from dotenv import  load_dotenv
import os
load_dotenv()
SECRET_KEY= os.getenv('SECRET_KEY')
import  secrets

print(secrets.token_urlsafe(32))