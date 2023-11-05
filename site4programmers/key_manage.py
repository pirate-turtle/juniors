from django.core.management.utils import get_random_secret_key


def get_secret_key():
    path = 'secret_key.txt'

    try:
        file = open(path, 'r')
        secret_key = file.read()
        file.close()

        # secret key의 길이가 50보다 적은 경우 재생성을 위해 에러 발생
        if len(secret_key) < 50:
            raise

    except:
        file = open(path, 'w')
        secret_key = get_random_secret_key()
        file.write(secret_key)

    return secret_key