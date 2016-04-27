from app import app as application
import logging
import config
import os

logging.basicConfig(filename=os.path.join(config.LOG_DIR, config.LOG_FILE_NAME), format=config.LOG_FORMAT,
                    level=logging.NOTSET)

if __name__ == "__main__":
    application.run(host=config.HOST_IP, port=config.HOST_PORT, debug=config.DEBUG)
