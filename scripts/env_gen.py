from django.core.management.utils import get_random_secret_key

CONFIG_STRING = """
SECRET_KEY='%s'
DEBUG=True
ALLOWED_HOSTS=.localhost, .127.0.0.1
DB_NAME=''
DB_USER=''
DB_PASSWORD=''
DB_HOST=''
DB_PORT=''
STATIC_ROOT=''
""".strip() % get_random_secret_key()

# Writing our configuration file to '.env'
with open('.env', 'w') as env:
    env.write(CONFIG_STRING)
    print('\n .env has been generated \n')
