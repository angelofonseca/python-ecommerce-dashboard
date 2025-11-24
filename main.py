from rich.console import Console
from products.product import search_products
from products.product import create_product
from products.product import update_product
from products.product import delete_product
from products.product import list_products
from products.graphs import products_by_brand
from products.graphs import products_by_category
from products.graphs import products_by_price_range
from sales.graphs import sales_by_status
from sales.graphs import sales_by_date
from sales.graphs import sales_by_day
from sales.sale import create_sale
from sales.sale import cancel_sale
from sales.sale import list_sales
from sales.sale import update_sale_status


console = Console()


while True:
    console.print("[purple3]1. Produtos")
    console.print("[purple3]2. Pedidos")
    console.print("[purple3]3. Pesquisas Avançadas")
    console.print("[purple3]4. Gráficos")
    console.print("[purple3]5. Finalizar")
    opcao = int(console.input("[purple3]Opção: "))
    if opcao == 1:
        print()
        console.rule("Produtos")
        console.print("1. Novo", style="green3")
        console.print("2. Atualizar", style="green3")
        console.print("3. Excluir", style="green3")
        console.print("4. Produtos", style="green3")
        console.print("5. Retornar", style="chartreuse4")
        opcao = int(console.input("Opção: "))
        if opcao == 1:
            create_product()
        elif opcao == 2:
            update_product()
        elif opcao == 3:
            delete_product()
        elif opcao == 4:
            list_products()
    elif opcao == 2:
        print()
        console.rule("Pedidos")
        console.print("1. Novo", style="green3")
        console.print("2. Cancelar", style="green3")
        console.print("3. Pedidos", style="green3")
        console.print("4. Atualizar Status", style="green3")
        console.print("5. Retornar", style="chartreuse4")
        opcao = int(console.input("Opção: "))
        if opcao == 1:
            create_sale()
        elif opcao == 2:
            cancel_sale()
        elif opcao == 3:
            list_sales()
        elif opcao == 4:
            update_sale_status()
    elif opcao == 3:
        print()
        console.rule("Pesquisar")
        console.print("1. Produtos", style="green3")
        console.print("2. Retornar", style="chartreuse4")
        opcao = int(console.input("Opção: "))
        if opcao == 1:
            search_products()
    elif opcao == 4:
        print()
        console.rule("Gráficos de Produtos e Pedidos/Vendas")
        console.print("1. Produtos por Marca", style="dark_orange3")
        console.print("2. Produtos por Categoria", style="dark_orange3")
        console.print("3. Produtos por Faixa de Preço", style="dark_orange3")
        console.print("4. Pedidos por Status", style="dark_orange3")
        console.print("5. Vendas por Mês", style="dark_orange3")
        console.print("6. Vendas por Dia", style="dark_orange3")
        console.print("7. Retornar", style="dark_orange3")
        opcao = int(console.input("Opção: "))
        if opcao == 1:
            products_by_brand()
        elif opcao == 2:
            products_by_category()
        elif opcao == 3:
            products_by_price_range()
        elif opcao == 4:
            sales_by_status()
        elif opcao == 5:
            sales_by_date()
        elif opcao == 6:
            sales_by_day()
    else:
        break
