import requests

create_url = "http://localhost:8080/checkout/create-session"
sales_url = "http://localhost:8080/sales"


def create(sale_data):
    try:
        response = requests.post(create_url, json=sale_data)
        response.raise_for_status()

        if response.status_code == 200:
            return (True, "Venda criada com sucesso!", response.json())
        else:
            return (False, "Falha ao criar a venda.", None)
    except requests.RequestException as e:
        return (False, f"Erro ao criar venda: {e}", None)


def find_all(params=None):
    if params is None:
        params = {}

    try:
        response = requests.get(sales_url, params=params)
        response.raise_for_status()
        result = response.json()

        if isinstance(result, dict) and "data" in result:
            return result["data"] if result["data"] else []

        return result if result else []
    except requests.RequestException as e:
        print(f"Erro ao buscar vendas: {e}")
        return None


def find_by_id(sale_id):
    try:
        response = requests.get(f"{sales_url}/{sale_id}")
        response.raise_for_status()
        result = response.json()

        if isinstance(result, dict) and "data" in result:
            return result["data"] if result["data"] else None

        return result if result else None
    except requests.RequestException as e:
        print(f"Erro ao buscar venda: {e}")
        return None


def update_status(sale_id, new_status):
    try:
        response = requests.patch(
            f"{sales_url}/{sale_id}/status", json={"status": new_status}
        )
        response.raise_for_status()

        if response.status_code == 200:
            return (True, "Status atualizado com sucesso!")
        else:
            return (False, "Falha ao atualizar status.")
    except requests.RequestException as e:
        return (False, f"Erro ao atualizar status: {e}")


def cancel(sale_id):
    try:
        response = requests.delete(f"{sales_url}/{sale_id}")
        response.raise_for_status()

        if response.status_code in [200, 204]:
            return (True, "Venda cancelada com sucesso!")
        else:
            return (False, "Falha ao cancelar a venda.")
    except requests.RequestException as e:
        return (False, f"Erro ao cancelar venda: {e}")
