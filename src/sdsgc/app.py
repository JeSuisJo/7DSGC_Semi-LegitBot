"""Entry point: check the config, then open the menu."""

from .setup import ensure_config


def main():
    ensure_config()

    # Imported here, not at module level: creating the driver reads config.json,
    # which the wizard above may have just written.
    from .cli import main as menu

    menu()


if __name__ == "__main__":
    main()
