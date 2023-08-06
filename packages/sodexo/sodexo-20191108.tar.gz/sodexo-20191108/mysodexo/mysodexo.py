#!/usr/bin/env python3
import os
import re

import requests
from lxml import html

DASHBOARD_URL = "https://www.mysodexo.es/mis-servicios-tarjetas"
LOGIN_URL = "https://www.mysodexo.es/lib/login.php"


def login(email: str, password: str) -> requests.sessions.Session:
    session = requests.session()
    data = {
        "usr": email,
        "pwd-login": password,
    }
    # TODO: handle wrong login
    session.post(LOGIN_URL, data, verify=False)
    return session


def get_dashboard(session):
    response = session.get(DASHBOARD_URL)
    return response.text


def parse_dashboard(dashboard_html):
    """
    >>> dashboard_html = (
    ...     '<html><body>'
    ...     '<div id="tarjeta-SaldoDisponible"> 13.37 € </div>'
    ...     '</body></html>')
    >>> parse_dashboard(dashboard_html)
    13.37
    """
    tree = html.fromstring(dashboard_html)
    balance_text = tree.xpath('//*[@id="tarjeta-SaldoDisponible"]/text()')[0]
    balance_text = re.findall(r"\d+\.\d+", balance_text)[0]
    return float(balance_text)


def main():
    email = os.environ.get("EMAIL")
    password = os.environ.get("PASSWORD")
    session = login(email, password)
    dashboard_html = get_dashboard(session)
    balance = parse_dashboard(dashboard_html)
    print(f"balance: {balance}")


if __name__ == "__main__":
    main()
