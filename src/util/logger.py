from datetime import datetime


class Logger:

    @staticmethod
    def log_info(message):
        print('{}:INFO:{}'.format(datetime.today().isoformat(), message))

    @staticmethod
    def log_error(message):
        print('{}:ERROR:{}'.format(datetime.today().isoformat(), message))
