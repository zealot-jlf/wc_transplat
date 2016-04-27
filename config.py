import os

DEBUG = True

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

LOG_DIR = BASE_DIR + "/tmp/"

LOG_FILE_NAME = "wc_app.log"

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

HOST_IP = "0.0.0.0"

HOST_PORT = 5000
