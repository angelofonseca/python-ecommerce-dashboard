from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table
from helper.helper import free_shipping_conversion
from products import crud

console = Console()
url = "http://localhost:8080/product"


def create_product():
    print("\n=== Criar Novo Produto ===\n")

    name = Prompt.ask("Nome do produto").strip()
    photo = Prompt.ask("URL da foto do produto (opcional)", default="").strip()
    description = Prompt.ask("Descrição do produto (opcional)", default="").strip()
    brand_id = int(Prompt.ask("ID da marca do produto").strip())
    category_id = int(Prompt.ask("ID da categoria do produto").strip())
    price = float(Prompt.ask("Preço do produto").strip())
    quantity = int(Prompt.ask("Quantidade em estoque").strip())

    product_data = {
        "name": name,
        "photo": photo,
        "description": description,
        "brandId": brand_id,
        "categoryId": category_id,
        "price": price,
        "quantity": quantity,
    }

    success, message, data = crud.create(product_data)

    if success:
        print(f"\n✅ {message}")
        if data:
            print(f"   ID do produto: {data['result']['id']}")
    else:
        print(f"\n❌ {message}")


def search_products():
    print("\n=== Buscar Produtos ===\n")

    brand = Prompt.ask("Informe a marca", default="").strip()
    category = Prompt.ask("Informe a categoria", default="").strip()
    free_shipping = Prompt.ask(
        "Informe se o frete é grátis (sim/não)", default=""
    ).strip()

    params = {}
    if brand:
        params["brandName"] = brand
    if category:
        params["categoryName"] = category
    if free_shipping:
        params["freeShipping"] = free_shipping_conversion(free_shipping)

    products = crud.find_all(params)

    if products is None:
        print("\n❌ Não foi possível realizar a busca. Tente novamente.")
        return

    if not products:
        print("\n⚠️  Nenhum produto encontrado com os critérios fornecidos.")
        return

    _display_products(products)


def list_products():
    print("\n=== Lista de Produtos ===\n")

    products = crud.find_all()

    if products is None:
        print("\n❌ Não foi possível buscar produtos. Tente novamente.")
        return

    if not products:
        print("\n⚠️  Nenhum produto cadastrado.")
        return

    _display_products(products)


def update_product():
    print("\n=== Atualizar Produto ===\n")

    product_id = Prompt.ask("ID do produto a ser atualizado").strip()

    current_product = crud.find_by_id(product_id)

    if current_product is None:
        print("\n❌ Erro ao buscar produto.")
        return

    if not current_product:
        print(f"\n⚠️  Produto com ID {product_id} não encontrado.")
        return

    print(f"\nProduto encontrado: {current_product['name']}")
    print("Deixe em branco para manter o valor atual.\n")

    name = Prompt.ask("Nome do produto", default=current_product["name"]).strip()

    photo = Prompt.ask("URL da foto", default=current_product.get("photo", "")).strip()

    description = Prompt.ask(
        "Descrição", default=current_product.get("description", "")
    ).strip()

    brand_id = Prompt.ask(
        "ID da marca", default=str(current_product["brandId"])
    ).strip()

    category_id = Prompt.ask(
        "ID da categoria", default=str(current_product["categoryId"])
    ).strip()

    price = Prompt.ask("Preço", default=str(current_product["price"])).strip()

    product_data = {
        "name": name,
        "photo": photo,
        "description": description,
        "brandId": int(brand_id),
        "categoryId": int(category_id),
        "price": float(price),
    }

    success, message = crud.update_by_id(product_id, product_data)

    if success:
        print(f"\n✅ {message}")
    else:
        print(f"\n❌ {message}")


def delete_product():
    print("\n=== Deletar Produto ===\n")

    product_id = Prompt.ask("ID do produto a ser deletado").strip()

    print("\nBuscando produto...")
    current_product = crud.find_by_id(product_id)

    if current_product is None:
        print("\n❌ Erro ao buscar produto.")
        return

    if not current_product:
        print(f"\n⚠️  Produto com ID {product_id} não encontrado.")
        return

    print("\nProduto encontrado:")
    print(f"  ID: {current_product['id']}")
    print(f"  Nome: {current_product['name']}")
    print(f"  Marca: {current_product['brand']['name']}")
    print(f"  Preço: R$ {current_product['price']:.2f}")

    confirm = (
        Prompt.ask("\n⚠️  Tem certeza que deseja deletar este produto? (sim/não)")
        .strip()
        .lower()
    )

    if confirm not in ["sim", "s"]:
        print("\n❌ Operação cancelada.")
        return

    success, message = crud.delete_by_id(product_id)

    if success:
        print(f"\n✅ {message}")
    else:
        print(f"\n❌ {message}")


def _display_products(products):
    """Exibe produtos em formato de tabela"""
    console.print(
        f"\n[bold cyan]{len(products)} produto(s) encontrado(s)[/bold cyan]\n"
    )

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", justify="center", style="cyan")
    table.add_column("Nome", style="white")
    table.add_column("Marca", style="yellow")
    table.add_column("Categoria", style="green")
    table.add_column("Preço", justify="right", style="bold green")
    table.add_column("Frete Grátis", justify="center", style="blue")
    table.add_column("Estoque", justify="center", style="magenta")

    for p in products:
        frete = "✓" if p.get("freeShipping") else "✗"
        frete_color = "green" if p.get("freeShipping") else "red"
        quantidade = p.get("stock", {}).get("quantity", "N/A")

        if quantidade == "N/A":
            estoque_color = "dim"
        elif quantidade == 0:
            estoque_color = "red"
        elif quantidade < 5:
            estoque_color = "yellow"
        else:
            estoque_color = "green"

        table.add_row(
            str(p["id"]),
            p["name"],
            p["brand"]["name"],
            p["category"]["name"],
            f"R$ {p['price']:.2f}",
            f"[{frete_color}]{frete}[/{frete_color}]",
            f"[{estoque_color}]{quantidade}[/{estoque_color}]",
        )

    console.print(table)
    console.input("\n[dim]Pressione Enter para continuar...[/dim]")
