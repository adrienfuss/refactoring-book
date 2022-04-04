import json
from typing import Dict, Any

from chapter_1.create_statement_data import create_statement_data

def usd(value: float) -> str:
    return f'${value / 100:,.2f}'

def html_statement(invoice: Dict[str, Any], plays: Dict[str, Any]) -> str:
    return render_html(create_statement_data(invoice, plays))


def statement(invoice: Dict[str, Any], plays: Dict[str, Any]) -> str:
    return render_plain_text(create_statement_data(invoice, plays))


def render_html(data):
    result = f"<h1>Statement for {data['customer']}</h1>\n"
    result += "<table>\n"
    result += "<tr><th>play</th><th>seats</th><th>cost</th></tr>"
    for a_performance in data['performances']:
        result += f'  <tr><td>{a_performance["play"]["name"]}</td><td>{a_performance["audience"]}</td>\n'
        result += f"<td>{usd(a_performance['amount'])}</td></tr>\n"
    result += "</table>\n"
    result += f'<p>Amount owed is <em>{usd(data["total_amount"])}</em></p>\n'
    result += f'<p>You earned <em>{data["total_volume_credits"]}</em> credits</p>\n'
    return result


def render_plain_text(data):
    result = f"Statement for {data['customer']}\n"
    for a_performance in data['performances']:
        result += f'    {a_performance["play"]["name"]}: {usd(a_performance["amount"])} ({a_performance["audience"]} seats)\n'
    result += f'Amount owed is {usd(data["total_amount"])}\n'
    result += f'You earned {data["total_volume_credits"]} credits\n'
    return result


def main():
    result = statement(
        json.load(open('data/invoices.json'))[0],
        json.load(open('data/plays.json')),
    )
    print(result)


if __name__ == '__main__':
    main()
