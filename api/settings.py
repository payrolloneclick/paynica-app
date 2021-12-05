import os

from environs import Env

# BASE PATH
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

env = Env()
ENV_FILE = env.str("ENV_FILE", default=".env")
env.read_env(os.path.join(BASE_DIR, ENV_FILE))

# ENV
TEST_ENV = env.bool("TEST_ENV", False)

# DB
DATABASE_URI = env.str("DATABASE_URI", None)

# JWT
JWT_SECRET_KEY = env.str("JWT_SECRET_KEY")
JWT_ACCESS_TOKEN_EXPIRED_AT = env.int("JWT_ACCESS_TOKEN_EXPIRED_AT")  # in sec
JWT_REFRESH_TOKEN_EXPIRED_AT = env.int("JWT_REFRESH_TOKEN_EXPIRED_AT")  # in sec
