import os
from dotenv import load_dotenv

PORT = 8088
LOG_LEVEL = 'INFO'

# Need to check and return boolean, so check for String "True"
print(os.environ.keys())
APP_ENVIRONMENT = os.environ.get('ENV') == 'development'

if APP_ENVIRONMENT:
    load_dotenv(".env.development")
else:
    load_dotenv(".env.production")

HOST = os.environ.get("HOST")

print(HOST)
