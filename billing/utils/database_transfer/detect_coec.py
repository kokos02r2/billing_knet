import chardet


def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        rawdata = f.read()
        result = chardet.detect(rawdata)
        return result.get('encoding')


print(detect_encoding('utils/database_transfer/csv/users_utf.csv'))
