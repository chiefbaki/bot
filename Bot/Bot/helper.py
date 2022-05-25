import datetime


class Log:
    def __init__(self, key: str = 'LOG', comment: str = '') -> None:
        if scfg.LOG_MODE:
            with open('data\log.txt', 'a') as f:
                f.write(f'{key} --- {str(datetime.datetime.now())} --- {comment}\n')


class Debug:
    def __init__(self, data: any = '', is_log: bool = True, key: str = 'LOG'):
            print(data)
            with open('data\log.txt', 'a') as f:
                f.write(f'{key} --- {str(datetime.datetime.now())} --- {data}\n')