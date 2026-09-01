from .setup import ensure_config


def main():
    ensure_config()

    from .cli import main as menu

    menu()


if __name__ == "__main__":
    main()
