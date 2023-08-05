import requests


def get_avatar(user):
    """
    Busca o avatar de usuário no Github

    :param usuario: str com o nome do usuário
    :return: str com o link do avatar do usuário
    """
    url = f'https://api.github.com/users/{user}'
    resp = requests.get(url)
    return resp.json()['avatar_url']


if __name__ == '__main__':
    print(get_avatar('rafaelhfreitas'))
