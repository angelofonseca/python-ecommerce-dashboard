import requests

url = "http://localhost:8080/product"


def create(data):
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()

        if response.status_code == 201:
            result = response.json()
            return (True, "Produto criado com sucesso!", result)
        else:
            return (False, "Falha ao criar o produto.", None)
    except requests.RequestException as e:
        return (False, f"Erro ao criar produto: {e}", None)


def find_all(params=None):

    if params is None:
        params = {}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        result = response.json()
        return result if result else []
    except requests.RequestException as e:
        print(f"Erro ao buscar produtos: {e}")
        return None


def find_by_id(id):
    try:
        response = requests.get(f"{url}/{id}")
        response.raise_for_status()
        result = response.json()
        return result if result else None
    except requests.RequestException as e:
        print(f"Erro ao buscar produto: {e}")
        return None


def update_by_id(id, data):
    try:
        response = requests.patch(f"{url}/{id}", json=data)
        response.raise_for_status()

        if response.status_code == 200:
            return (True, "Produto atualizado com sucesso!")
        else:
            return (False, "Falha ao atualizar o produto.")
    except requests.RequestException as e:
        return (False, f"Erro ao atualizar produto: {e}")


def delete_by_id(id):

    try:
        response = requests.delete(f"{url}/{id}")
        response.raise_for_status()
        if response.status_code == 200:
            return (True, "Produto deletado com sucesso!")
        else:
            return (False, "Falha ao deletar o produto.")
    except requests.RequestException as e:
        return (False, f"Erro ao deletar produto: {e}")
