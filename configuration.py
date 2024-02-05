from enum import Enum
import tomli


class Models(Enum):
    """
    Słownik modeli do wykorzystania
    dostęp w kodzie:
    Models.GPT_TURBO.value
    """
    GPT3 = "gpt-3.5-turbo-1106"
    GPT4 = "gpt-4-1106-preview"


def _get_config():
    """
    Module runs in context of the root folder with pyproject.toml file
    """
    with open("secrets.toml", "rb") as f:
        config = tomli.load(f)

    return config


_config = _get_config()
api_key = _config["API"]["key"]
assistant_id = _config["API"]["assistant_id"]
assistant_id3 = _config["API"]["assistant_id3"]
assistant_id4 = _config["API"]["assistant_id4"]

sender_passwords = _config["Mail"]["sender_passwords"]
user_mail = _config["Mail"]["user_mail"]

engine = _config["Engines"]["GPT4"]

airtable_token = _config["Airtable"]["airtable_token"]
base_id = _config["Airtable"]["base_id"]
table_id = _config["Airtable"]["table_id"]
table_id2 = _config["Airtable"]["table_id2"]

aws_access_key_id = _config["AWS"]["aws_access_key_id"]
aws_secret_access_key = _config["AWS"]["aws_secret_access_key"]

api_sa_key=_config['APISA']['api_sa_key']
api_sa_secret=_config['APISA']['api_sa_secret']
whereby_api_key=_config['WHEREBY']['api_key']
