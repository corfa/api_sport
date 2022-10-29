import os

from dotenv import load_dotenv

load_dotenv()


class ConfigApp:
    user = os.getenv("User", "root")
    dbPassword = os.getenv("Password", "9213")
    dbName = os.getenv("DB", "fitnes")
    dbHost = os.getenv("host", "localhost")
    port = os.getenv("port", "4000")
    url = rf'postgresql+psycopg2://{user}:{dbPassword}@{dbHost}/{dbName}'

