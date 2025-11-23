from rich.console import Console
from rich.table import Table
from sales.crud import find_all
from datetime import datetime
from collections import defaultdict

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


def sales_by_status():
    console.print("\n[bold cyan]═══ Gráfico de Vendas por Status ═══[/bold cyan]\n")

    try:
        vendas = find_all()

        if not vendas:
            console.print("[yellow]Nenhuma venda encontrada[/yellow]")
            return

        grupos = {}
        valores_por_status = {}

        for venda in vendas:
            status = venda.get("status", "UNKNOWN")
            grupos[status] = grupos.get(status, 0) + 1

            try:
                total = float(venda.get("totalValue", 0) or 0)
            except (ValueError, TypeError):
                total = 0.0
            valores_por_status[status] = valores_por_status.get(status, 0) + total

        total_vendas = sum(grupos.values())
        total_valor = sum(valores_por_status.values())

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Status", style="bold")
        table.add_column("Quantidade", justify="center")
        table.add_column("Percentual (%)", justify="center")
        table.add_column("Valor Total", justify="right")
        table.add_column("Gráfico")

        status_cores = {
            "PENDING": "yellow",
            "PROCESSING": "blue",
            "PAID": "green",
            "CANCELLED": "red",
            "REFUNDED": "orange_red1",
        }

        for status, num in sorted(grupos.items()):
            barra = "●" * int((num / total_vendas) * 100)
            percentual = (num / total_vendas) * 100
            valor = valores_por_status.get(status, 0)
            cor = status_cores.get(status, cores[0])

            table.add_row(
                f"[{cor}]{status}",
                f"[{cor}]{num}",
                f"[{cor}]{percentual:.1f}%",
                f"[{cor}]R$ {valor:.2f}",
                f"[{cor}]{barra}",
            )

        console.print(table)
        console.print(
            f"\n[dim]Total de vendas: {total_vendas} | "
            f"Valor total: R$ {total_valor:.2f}[/dim]"
        )

    except Exception as e:
        console.print(f"[bold red]Erro ao gerar gráfico: {e}[/bold red]")

    console.input("\n[dim]Pressione Enter para continuar...[/dim]")


def sales_by_date():
    console.print("\n[bold cyan]═══ Gráfico de Vendas por Mês ═══[/bold cyan]\n")

    try:
        vendas = find_all()

        if not vendas:
            console.print("[yellow]Nenhuma venda encontrada[/yellow]")
            return

        grupos = defaultdict(int)
        valores_por_mes = defaultdict(float)

        for venda in vendas:
            created_at = venda.get("createdAt")
            if not created_at:
                continue

            try:
                data = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                mes_ano = data.strftime("%Y-%m")

                grupos[mes_ano] += 1
                try:
                    valor = float(venda.get("totalValue", 0) or 0)
                except (ValueError, TypeError):
                    valor = 0.0
                valores_por_mes[mes_ano] += valor
            except (ValueError, AttributeError):
                continue

        if not grupos:
            console.print("[yellow]Nenhuma venda com data válida encontrada[/yellow]")
            return

        grupos_ordenados = sorted(grupos.items())

        max_valor = max(valores_por_mes.values())

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Mês/Ano", style="bold")
        table.add_column("Quantidade", justify="center")
        table.add_column("Valor Total", justify="right")
        table.add_column("Gráfico")

        for i, (mes_ano, num) in enumerate(grupos_ordenados):
            valor = valores_por_mes[mes_ano]
            if max_valor > 0:
                barra = "■" * int((valor / max_valor) * 50)
            else:
                barra = ""

            try:
                data_obj = datetime.strptime(mes_ano, "%Y-%m")
                mes_formatado = data_obj.strftime("%b/%Y")
            except ValueError:
                mes_formatado = mes_ano

            table.add_row(
                f"[{cores[i%n_cores]}]{mes_formatado}",
                f"[{cores[i%n_cores]}]{num}",
                f"[{cores[i%n_cores]}]R$ {valor:.2f}",
                f"[{cores[i%n_cores]}]{barra}",
            )

        total_vendas = sum(grupos.values())
        total_valor = sum(valores_por_mes.values())

        console.print(table)
        console.print(
            f"\n[dim]Total de vendas: {total_vendas} | "
            f"Valor total: R$ {total_valor:.2f}[/dim]"
        )

    except Exception as e:
        console.print(f"[bold red]Erro ao gerar gráfico: {e}[/bold red]")

    console.input("\n[dim]Pressione Enter para continuar...[/dim]")


def sales_by_day():
    console.print("\n[bold cyan]═══ Gráfico de Vendas por Dia ═══[/bold cyan]\n")

    try:
        vendas = find_all()

        if not vendas:
            console.print("[yellow]Nenhuma venda encontrada[/yellow]")
            return

        grupos = defaultdict(int)
        valores_por_dia = defaultdict(float)

        for venda in vendas:
            created_at = venda.get("createdAt")
            if not created_at:
                continue

            try:
                data = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                dia = data.strftime("%Y-%m-%d")

                grupos[dia] += 1
                try:
                    valor = float(venda.get("totalValue", 0) or 0)
                except (ValueError, TypeError):
                    valor = 0.0
                valores_por_dia[dia] += valor
            except (ValueError, AttributeError):
                continue

        if not grupos:
            console.print("[yellow]Nenhuma venda com data válida encontrada[/yellow]")
            return

        grupos_ordenados = sorted(grupos.items())[-30:]

        max_valor = max([valores_por_dia[dia] for dia, _ in grupos_ordenados])

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Data", style="bold")
        table.add_column("Qtde", justify="center")
        table.add_column("Valor Total", justify="right")
        table.add_column("Gráfico")

        for i, (dia, num) in enumerate(grupos_ordenados):
            valor = valores_por_dia[dia]
            if max_valor > 0:
                barra = "■" * int((valor / max_valor) * 40)
            else:
                barra = ""

            try:
                data_obj = datetime.strptime(dia, "%Y-%m-%d")
                dia_formatado = data_obj.strftime("%d/%m/%Y")
            except ValueError:
                dia_formatado = dia

            table.add_row(
                f"[{cores[i%n_cores]}]{dia_formatado}",
                f"[{cores[i%n_cores]}]{num}",
                f"[{cores[i%n_cores]}]R$ {valor:.2f}",
                f"[{cores[i%n_cores]}]{barra}",
            )

        console.print(table)

    except Exception as e:
        console.print(f"[bold red]Erro ao gerar gráfico: {e}[/bold red]")

    console.input("\n[dim]Pressione Enter para continuar...[/dim]")


def sales_graphs_menu():
    while True:
        console.clear()
        console.print("[bold cyan]═══════════════════════════════════════[/bold cyan]")
        console.print("[bold cyan]     GRÁFICOS DE VENDAS                [/bold cyan]")
        console.print(
            "[bold cyan]═══════════════════════════════════════[/bold cyan]\n"
        )

        console.print("[1] Vendas por Status")
        console.print("[2] Vendas por Mês")
        console.print("[3] Vendas por Dia (últimos 30 dias)")
        console.print("[0] Voltar")

        opcao = console.input("\n[dim]Escolha uma opção: [/dim]")

        if opcao == "1":
            sales_by_status()
        elif opcao == "2":
            sales_by_date()
        elif opcao == "3":
            sales_by_day()
        elif opcao == "0":
            break
        else:
            console.print("[yellow]Opção inválida![/yellow]")
            console.input("\n[dim]Pressione Enter para continuar...[/dim]")
