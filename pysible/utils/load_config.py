from dotenv import dotenv_values


def load_config():
    config = dotenv_values(".env")

    return config
