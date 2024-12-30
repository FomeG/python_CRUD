import json

with open('Web/appsettings.json') as config_file:
    config = json.load(config_file)

class Config_db:
    # Database config
    cf = config["ConnectionStrings"]
    SQLALCHEMY_DATABASE_URI = f"postgresql://{cf['user']}:{cf['password']}@{cf['host']}:{cf['port']}/{cf['dbname']}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False