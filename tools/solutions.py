"""Управление видимостью страниц «Решение N» на docs.langfuse-workshop.ru.

Примеры:
    python tools/solutions.py status
    python tools/solutions.py hide all
    python tools/solutions.py show 1 2
    python tools/solutions.py sync      # пересобрать сайт, если он разошелся с настройкой

Утилита по SSH записывает список скрытых страниц в hidden_solutions.txt на сервере
и пересобирает контейнер с документацией (см. hooks/hide_solutions.py).
"""
import argparse
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request

HOST = os.getenv("WORKSHOP_DOCS_HOST", "root@5.129.199.163")
SSH_KEY = os.getenv("WORKSHOP_DOCS_SSH_KEY", r"C:\dev\keys\deploy_key")
REMOTE_DIR = "/root/docs-langfuse-workshop"
HIDDEN_FILE = "hidden_solutions.txt"
SITE_URL = "https://docs.langfuse-workshop.ru"

SOLUTIONS = [1, 2, 3, 4, 5]


def page_file(n):
    return f"step{n}2.md"


def ssh(command, input_text=None):
    result = subprocess.run(
        ["ssh", "-o", "BatchMode=yes", "-o", "IdentitiesOnly=yes", "-i", SSH_KEY, HOST, command],
        input=input_text, capture_output=True, text=True, encoding="utf-8",
    )
    if result.returncode != 0:
        sys.exit(f"Ошибка SSH ({result.returncode}): {result.stderr.strip()}")
    return result.stdout


def read_hidden():
    out = ssh(f"cat {REMOTE_DIR}/{HIDDEN_FILE} 2>/dev/null || true")
    return {line.strip() for line in out.splitlines() if line.strip()}


def write_hidden(hidden):
    path = f"{REMOTE_DIR}/{HIDDEN_FILE}"
    if hidden:
        ssh(f"cat > {path}", input_text="".join(f"{name}\n" for name in sorted(hidden)))
    else:
        ssh(f"rm -f {path}")


def rebuild(hidden):
    print("Пересобираю документацию на сервере...")
    started = time.time()
    ssh(f"cd {REMOTE_DIR} && docker compose up -d --build --quiet-pull 2>&1 && docker image prune -f >/dev/null")
    # новый контейнер начинает отвечать не сразу - ждем, пока сайт придет в нужное состояние
    deadline = time.time() + 30
    while not site_matches(hidden) and time.time() < deadline:
        time.sleep(2)
    print(f"Готово за {time.time() - started:.0f} с")


def page_status(n):
    # что реально видит участник: 200 - страница открывается, 404 - скрыта
    url = f"{SITE_URL}/step{n}2/"
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            return response.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return None


def expected_status(n, hidden):
    return 404 if page_file(n) in hidden else 200


def site_matches(hidden):
    return all(page_status(n) == expected_status(n, hidden) for n in SOLUTIONS)


def print_status(hidden):
    in_sync = True
    for n in SOLUTIONS:
        state = "скрыто" if page_file(n) in hidden else "видно"
        code = page_status(n)
        line = f"Решение {n}: {state}  (сайт отвечает {code or 'ошибкой'})"
        if code != expected_status(n, hidden):
            in_sync = False
            line += "  <- сайт не совпадает с настройкой"
        print(line)
    if not in_sync:
        print("Сайт не пересобран под текущую настройку, выполните: python tools/solutions.py sync")


def parse_numbers(values):
    if values == ["all"]:
        return SOLUTIONS
    try:
        numbers = [int(v) for v in values]
    except ValueError:
        sys.exit("Укажите номера решений (1-5) или all")
    unknown = [n for n in numbers if n not in SOLUTIONS]
    if unknown:
        sys.exit(f"Нет таких решений: {unknown}")
    return numbers


def main():
    parser = argparse.ArgumentParser(description="Видимость страниц «Решение N» на сайте воркшопа")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status", help="показать, какие решения скрыты")
    sub.add_parser("sync", help="пересобрать сайт под текущую настройку")
    for name, help_text in [("hide", "скрыть решения"), ("show", "показать решения")]:
        p = sub.add_parser(name, help=help_text)
        p.add_argument("numbers", nargs="+", help="номера решений 1-5 или all")
    args = parser.parse_args()

    hidden = read_hidden()
    if args.command == "status":
        print_status(hidden)
        return
    if args.command == "sync":
        rebuild(hidden)
        print_status(hidden)
        return

    pages = {page_file(n) for n in parse_numbers(args.numbers)}
    new_hidden = hidden | pages if args.command == "hide" else hidden - pages
    if new_hidden != hidden:
        write_hidden(new_hidden)
    # пересобираем и тогда, когда настройка не изменилась, но сайт ей не соответствует:
    # например, если прошлая пересборка оборвалась после записи файла
    if new_hidden != hidden or not site_matches(new_hidden):
        rebuild(new_hidden)
    else:
        print("Ничего не изменилось")
    print_status(new_hidden)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
