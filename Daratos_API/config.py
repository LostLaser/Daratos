from os import environ as env
import multiprocessing

PORT = int(env.get("PORT", 8080))
MIN_TEXT_LENGTH = 300
DEBUG_MODE = int(env.get("DEBUG_MODE", 1))
DB_CONFIG_PATH = str(env.get("DB_CONFIG_PATH", "./db_config.json"))
PREDICTION_API_URL = str(env.get("PREDICTION_URL","https://api.thebipartisanpress.com/api/endpoints/daratos/bert/"))
PREDICTION_API_KEY = str(env.get("PREDICTION_API_KEY", ""))
if not PREDICTION_API_KEY:
    print("ERROR: Missing PREDICTION_API_KEY" + PREDICTION_API_KEY)
    exit()

# Gunicorn config
bind = ":" + str(PORT)