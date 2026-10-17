# Скрывает страницы решений, чтобы участники воркшопа не забегали вперед.
# Список скрытых страниц лежит в hidden_solutions.txt рядом с mkdocs.yml (по имени файла в строке).
# Файл есть только на сервере и управляется утилитой tools/solutions.py; без него видны все страницы.
import logging
import os

HIDDEN_FILE = "hidden_solutions.txt"

log = logging.getLogger("mkdocs.hooks.hide_solutions")
hidden = set()


def on_config(config):
    path = os.path.join(os.path.dirname(config.config_file_path), HIDDEN_FILE)
    hidden.clear()
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            hidden.update(line.strip() for line in f if line.strip())

    if hidden:
        log.info("Скрытые страницы: %s", ", ".join(sorted(hidden)))
        # пункты меню вида {"Решение 1": "step12.md"}
        config.nav = [
            item for item in config.nav
            if not (isinstance(item, dict) and hidden & set(item.values()))
        ]
    return config


def on_files(files, config):
    # скрытые страницы не попадают на сайт и в поиск: по прямой ссылке будет 404
    for file in list(files):
        if file.src_uri in hidden:
            files.remove(file)
    return files
