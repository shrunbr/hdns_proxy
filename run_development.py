import os

os.environ['FLASK_ENV'] = 'development'

if __name__ == "__main__":
    os.system("flask run -h 0.0.0.0 -p 8080")