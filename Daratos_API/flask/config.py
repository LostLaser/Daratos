from os import environ as env
import multiprocessing

PORT = int(env.get("PORT", 8080))
DEBUG_MODE = int(env.get("DEBUG_MODE", 1))
MODEL_PATH = str(env.get("MODEL_PATH", "./sentenceModel.h5"))
TOKENIZER_PATH = str(env.get("TOKENIZER_PATH", "./tokenizer.pickle"))
DB_CONFIG_PATH = str(env.get("DB_CONFIG_PATH", "./api_config.json"))

# Gunicorn config
bind = ":" + str(PORT)
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2 * multiprocessing.cpu_count()