from rich.prompt import Prompt, IntPrompt, Confirm
from rich.console import Console
from rich.table import Table
from sales import crud
from products import crud as product_crud

console = Console()

def create_sale():
    console.print("\n[bold cyan]=== Criar Nova Venda ===[/bold cyan]\n")

    user_id = IntPrompt.ask("ID do usuário")
    shipping_address = Prompt.ask("Endereço de entrega").strip()

    console.print("\n[yellow]Métodos de pagamento:[/yellow]")
    console.print("1. CREDIT_CARD")
    console.print("2. PIX")
    console.print("3. BOLETO")
    payment_choice = IntPrompt.ask("Escolha o método", choices=["1", "2", "3"])

    payment_methods = {1: "CREDIT_CARD", 2: "PIX", 3: "BOLETO"}
    payment_method = payment_methods[payment_choice]

    items = []
    console.print("\n[bold green]Adicionar itens ao pedido[/bold green]")

    while True:
        console.print(f"\n[cyan]Item #{len(items) + 1}[/cyan]")

        product_id = IntPrompt.ask("ID do produto")

        console.print("[yellow]Buscando produto...[/yellow]")
        product = product_crud.find_by_id(product_id)

        if product is None:
            console.print("[red]❌ Erro ao buscar produto.[/red]")
            retry = Confirm.ask("Tentar outro produto?", default=True)
            if retry:
                continue
            else:
                break

        if not product:
            console.print(f"[red]❌ Produto com ID {product_id} não encontrado.[/red]")
            retry = Confirm.ask("Tentar outro produto?", default=True)
            if retry:
                continue
            else:
                break

        product_name = product["name"]
        price_unit = float(product["price"])
        stock_qty = product.get("stock", {}).get("quantity", 0)

        console.print(f"[green]✓ Produto encontrado:[/green]")
        console.print(f"  Nome: {product_name}")
        console.print(f"  Preço: R$ {price_unit:.2f}")
        console.print(f"  Estoque: {stock_qty} unidades")

        quantity = IntPrompt.ask(f"Quantidade (máx: {stock_qty})", default=1)

        if quantity > stock_qty:
            console.print(
                f"[red]⚠️  Quantidade maior que estoque disponível ({stock_qty}).[/red]"
            )
            use_available = Confirm.ask(
                f"Usar quantidade disponível ({stock_qty})?", default=True
            )
            if use_available:
                quantity = stock_qty
            else:
                continue

        items.append(
            {
                "productId": product_id,
                "productName": product_name,
                "quantity": quantity,
                "priceUnit": price_unit,
            }
        )

        console.print(
            f"[green]✓ Item adicionado! Subtotal: R$ {quantity * price_unit:.2f}[/green]"
        )

        add_more = Confirm.ask("\nAdicionar mais itens?", default=False)
        if not add_more:
            break

    if not items:
        console.print("\n[red]❌ Nenhum item adicionado. Venda cancelada.[/red]")
        return

    sale_data = {
        "userId": user_id,
        "shippingAddress": shipping_address,
        "paymentMethod": payment_method,
        "items": items,
    }

    console.print("\n[bold yellow]═══ Resumo do Pedido ═══[/bold yellow]")
    console.print(f"Usuário ID: {user_id}")
    console.print(f"Endereço: {shipping_address}")
    console.print(f"Pagamento: {payment_method}")
    console.print(f"\n[bold]Itens ({len(items)}):[/bold]")

    for i, item in enumerate(items, 1):
        subtotal = item["quantity"] * item["priceUnit"]
        console.print(
            f"  {i}. {item['productName']} - "
            f"{item['quantity']}x R$ {item['priceUnit']:.2f} = "
            f"R$ {subtotal:.2f}"
        )

    total = sum(item["quantity"] * item["priceUnit"] for item in items)
    console.print(f"\n[bold green]Valor Total: R$ {total:.2f}[/bold green]")
    print(items)
    confirm = Confirm.ask("\n[bold]Confirmar criação da venda?[/bold]", default=True)
    if not confirm:
        console.print("\n[red]❌ Operação cancelada.[/red]")
        return

    success, message, data = crud.create(sale_data)

    if success:
        console.print(f"\n[green]✅ {message}[/green]")
        if data and "result" in data:
            sale_id = data["result"]["id"]
            console.print(f"   [cyan]ID da venda: {sale_id}[/cyan]")
    else:
        console.print(f"\n[red]❌ {message}[/red]")


def list_sales():
    console.print("\n[bold cyan]=== Lista de Pedidos ===[/bold cyan]\n")

    sales = crud.find_all()

    if sales is None:
        console.print("\n[red]❌ Não foi possível buscar os pedidos.[/red]")
        return

    if not sales:
        console.print("\n[yellow]⚠️  Nenhuma venda cadastrada.[/yellow]")
        return

    _display_sales(sales)

def update_sale_status():
    console.print("\n[bold cyan]=== Atualizar Status da Venda ===[/bold cyan]\n")

    sale_id = IntPrompt.ask("ID da venda")

    current_sale = crud.find_by_id(sale_id)

    if current_sale is None:
        console.print("\n[red]❌ Erro ao buscar venda.[/red]")
        return

    if not current_sale:
        console.print(f"\n[yellow]⚠️  Venda com ID {sale_id} não encontrada.[/yellow]")
        return

    console.print(f"\n[cyan]Venda encontrada:[/cyan]")
    console.print(f"ID: {current_sale['id']}")
    console.print(f"Status atual: [yellow]{current_sale['status']}[/yellow]")
    console.print(f"Valor: R$ {float(current_sale['totalValue']):.2f}")

    console.print("\n[yellow]Novo status:[/yellow]")
    console.print("1. PENDING")
    console.print("2. PROCESSING")
    console.print("3. PAID")
    console.print("4. CANCELLED")
    console.print("5. REFUNDED")

    choice = IntPrompt.ask("Escolha o novo status", choices=["1", "2", "3", "4", "5"])

    statuses = {1: "PENDING", 2: "PROCESSING", 3: "PAID", 4: "CANCELLED", 5: "REFUNDED"}
    new_status = statuses[choice]

    confirm = Confirm.ask(
        f"\nAlterar status de {current_sale['status']} para {new_status}?", default=True
    )

    if not confirm:
        console.print("\n[red]❌ Operação cancelada.[/red]")
        return

    success, message = crud.update_status(sale_id, new_status)

    if success:
        console.print(f"\n[green]✅ {message}[/green]")
    else:
        console.print(f"\n[red]❌ {message}[/red]")


def cancel_sale():
    console.print("\n[bold cyan]=== Cancelar Venda ===[/bold cyan]\n")

    sale_id = IntPrompt.ask("ID da venda a ser cancelada")

    current_sale = crud.find_by_id(sale_id)

    if current_sale is None:
        console.print("\n[red]❌ Erro ao buscar venda.[/red]")
        return

    if not current_sale:
        console.print(f"\n[yellow]⚠️  Venda com ID {sale_id} não encontrada.[/yellow]")
        return

    console.print("\n[cyan]Venda encontrada:[/cyan]")
    console.print(f"ID: {current_sale['id']}")
    console.print(f"Usuário ID: {current_sale['userId']}")
    console.print(f"Status: {current_sale['status']}")
    console.print(f"Valor: R$ {float(current_sale['totalValue']):.2f}")

    confirm = Confirm.ask(
        "\n[red]⚠️  Tem certeza que deseja cancelar esta venda?[/red]", default=False
    )

    if not confirm:
        console.print("\n[red]❌ Operação cancelada.[/red]")
        return

    success, message = crud.cancel(sale_id)

    if success:
        console.print(f"\n[green]✅ {message}[/green]")
    else:
        console.print(f"\n[red]❌ {message}[/red]")

def _display_sales(sales):
    console.print(f"\n[bold]{len(sales)} venda(s) encontrada(s):[/bold]\n")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="cyan", justify="right")
    table.add_column("Cliente", style="white")
    table.add_column("Status", style="yellow")
    table.add_column("Pagamento")
    table.add_column("Itens", justify="right")
    table.add_column("Valor Total", justify="right", style="green")
    table.add_column("Data")

    for sale in sales:
        user_name = "N/A"
        if "user" in sale and sale["user"]:
            user_name = sale["user"].get("name", f"ID: {sale['userId']}")
        else:
            user_name = f"ID: {sale['userId']}"

        items_count = len(sale.get("orders", []))

        created_date = sale["createdAt"][:10] if "createdAt" in sale else "N/A"

        table.add_row(
            str(sale["id"]),
            user_name,
            sale["status"],
            sale.get("paymentMethod", "N/A"),
            str(items_count),
            f"R$ {float(sale['totalValue']):.2f}",
            created_date,
        )

    console.print(table)
