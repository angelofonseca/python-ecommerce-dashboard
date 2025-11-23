from rich.console import Console
from rich.table import Table
from products.crud import find_all

console = Console()

cores = [
    "green1",
    "sky_blue2",
    "deep_pink4",
    "orange_red1",
    "gold1",
    "cyan1",
    "magenta1",
    "yellow1",
    "orchid1",
    "spring_green1",
]
n_cores = len(cores)


def products_by_brand():
    console.print("\n[bold cyan]═══ Gráfico de Produtos por Marca ═══[/bold cyan]\n")

    try:
        produtos = find_all()

        if not produtos:
            console.print("[yellow]Nenhum produto encontrado[/yellow]")
            return

        grupos = {}
        for produto in produtos:
            marca = produto["brand"]["name"]
            grupos[marca] = grupos.get(marca, 0) + 1

        max_num = max(grupos.values())

        for i, (marca, num) in enumerate(sorted(grupos.items())):
            barra = "■" * int((num / max_num) * 50)
            console.print(f"[{cores[i%n_cores]}]{marca:20s} {barra} {num}")

        console.print(
            f"\n[dim]Total de marcas: {len(grupos)} | Total de produtos: {len(produtos)}[/dim]"
        )

    except Exception as e:
        console.print(f"[bold red]Erro ao gerar gráfico: {e}[/bold red]")

    console.input("\n[dim]Pressione Enter para continuar...[/dim]")


def products_by_category():
    console.print(
        "\n[bold cyan]═══ Gráfico de Produtos por Categoria ═══[/bold cyan]\n"
    )

    try:
        produtos = find_all()

        if not produtos:
            console.print("[yellow]Nenhum produto encontrado[/yellow]")
            return

        grupos = {}
        for produto in produtos:
            categoria = produto["category"]["name"]
            grupos[categoria] = grupos.get(categoria, 0) + 1

        total = sum(grupos.values())

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Categoria", style="bold")
        table.add_column("Quantidade", justify="center")
        table.add_column("Percentual (%)", justify="center")
        table.add_column("Gráfico")

        for i, (categoria, num) in enumerate(sorted(grupos.items())):
            barra = "●" * int((num / total) * 100)
            percentual = (num / total) * 100

            table.add_row(
                f"[{cores[i%n_cores]}]{categoria}",
                f"[{cores[i%n_cores]}]{num}",
                f"[{cores[i%n_cores]}]{percentual:.1f}%",
                f"[{cores[i%n_cores]}]{barra}",
            )

        console.print(table)
        console.print(
            f"\n[dim]Total de categorias: {len(grupos)} | Total de produtos: {total}[/dim]"
        )

    except Exception as e:
        console.print(f"[bold red]Erro ao gerar gráfico: {e}[/bold red]")

    console.input("\n[dim]Pressione Enter para continuar...[/dim]")


def products_by_price_range():
    console.print(
        "\n[bold cyan]═══ Gráfico de Produtos por Faixa de Preço ═══[/bold cyan]\n"
    )

    try:
        produtos = find_all()

        if not produtos:
            console.print("[yellow]Nenhum produto encontrado[/yellow]")
            return

        faixas = {
            "Até R$ 50": (0, 50),
            "R$ 51 - R$ 100": (51, 100),
            "R$ 101 - R$ 200": (101, 200),
            "R$ 201 - R$ 500": (201, 500),
            "Acima de R$ 500": (501, float("inf")),
        }

        grupos = {faixa: 0 for faixa in faixas.keys()}

        for produto in produtos:
            preco = produto["price"]
            for faixa, (min_preco, max_preco) in faixas.items():
                if min_preco <= preco <= max_preco:
                    grupos[faixa] += 1
                    break

        max_num = max(grupos.values()) if max(grupos.values()) > 0 else 1

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Faixa de Preço", style="bold")
        table.add_column("Quantidade", justify="center")
        table.add_column("Gráfico")

        for i, (faixa, num) in enumerate(grupos.items()):
            barra = "■" * int((num / max_num) * 40) if num > 0 else ""

            table.add_row(
                f"[{cores[i%n_cores]}]{faixa}",
                f"[{cores[i%n_cores]}]{num}",
                f"[{cores[i%n_cores]}]{barra}",
            )

        console.print(table)
        console.print(f"\n[dim]Total de produtos: {len(produtos)}[/dim]")

    except Exception as e:
        console.print(f"[bold red]Erro ao gerar gráfico: {e}[/bold red]")

    console.input("\n[dim]Pressione Enter para continuar...[/dim]")


def products_graphs_menu():
    while True:
        console.clear()
        console.print("[bold cyan]═══════════════════════════════════════[/bold cyan]")
        console.print("[bold cyan]     GRÁFICOS DE PRODUTOS              [/bold cyan]")
        console.print(
            "[bold cyan]═══════════════════════════════════════[/bold cyan]\n"
        )

        console.print("[1] Produtos por Marca")
        console.print("[2] Produtos por Categoria")
        console.print("[3] Produtos por Faixa de Preço")
        console.print("[0] Voltar")

        opcao = console.input("\n[dim]Escolha uma opção: [/dim]")

        if opcao == "1":
            products_by_brand()
        elif opcao == "2":
            products_by_category()
        elif opcao == "3":
            products_by_price_range()
        elif opcao == "0":
            break
        else:
            console.print("[yellow]Opção inválida![/yellow]")
            console.input("\n[dim]Pressione Enter para continuar...[/dim]")
