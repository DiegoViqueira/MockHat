#!/usr/bin/env python
import sys
import argparse
import subprocess
from pathlib import Path

# Añadir el directorio raíz del proyecto al path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))


LOCALE_DIR = "app/i18n/locales"


def compile_translations():
    """Compila todos los archivos PO a archivos MO."""
    print("Compilando traducciones...")
    subprocess.run(["pybabel", "compile", "-d", LOCALE_DIR], check=True)


def init_language(lang):
    """Inicializa un nuevo idioma."""
    print(f"Inicializando idioma {lang}...")
    subprocess.run(["pybabel", "init", "-i",
                   f"{LOCALE_DIR}/messages.pot", "-d", LOCALE_DIR, "-l", lang], check=True)


def main():
    parser = argparse.ArgumentParser(
        description="Herramientas de internacionalización")
    subparsers = parser.add_subparsers(
        dest="command", help="Comando a ejecutar")
    # Comando extract
    # Comando compile
    compile_parser = subparsers.add_parser(
        "compile", help="Compilar traducciones")
    # Comando init
    init_parser = subparsers.add_parser(
        "init", help="Inicializar un nuevo idioma (requiere CÓDIGO_IDIOMA como 'en', 'fr', 'es')")

    init_parser.add_argument("lang", help="Código del idioma (ej. 'en', 'fr')")

    args = parser.parse_args()

    if args.command == "compile":
        compile_translations()
    elif args.command == "init":
        init_language(args.lang)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
