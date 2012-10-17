from pymacco.ui.simpleCli import SimpleCli
from pymacco.ui.base import start

if __name__ == "__main__":
    try:
        start(SimpleCli)
    except KeyboardInterrupt:
        pass
