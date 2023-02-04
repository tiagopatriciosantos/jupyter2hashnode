"""jupyter2hashnode entry point script."""

from jupyter2hashnode import cli, __app_name__

def main():
    cli.app(prog_name=__app_name__)

if __name__ == "__main__":
    main()