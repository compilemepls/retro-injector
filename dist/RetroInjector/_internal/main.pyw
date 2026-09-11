import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    from retro.interface.window import MainWindow
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()