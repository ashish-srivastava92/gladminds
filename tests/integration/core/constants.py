def add_slashes(data):
    if data.startswith('/'):
        data = data[1:]
    if not data.endswith('/'):
        data = data + '/'

    return data


class AfterbuyUrls():
        REGISTRATION = 'consumers/registration/'

