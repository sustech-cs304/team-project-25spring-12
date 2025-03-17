from datetime import timedelta
import os

DATABASE_URL = os.environ.get('MJC_DATABASE_URL')

# JWT Security Settings
SECRET_KEY = os.environ.get('MJC_SECRET_KEY')
JWT_ENCODE_ALGORITHM = 'HS256'
TOKEN_EXPIRE_MINUTES = timedelta(minutes=1800)