from app import app
import os

app.config['ENV'] = "development"

if __name__ == "__main__":
    app.run(use_reloader=False)
