from datetime import datetime


def log(msg):
    print("[System] -", datetime.now(), "-", msg)


if __name__ == '__main__':
    log("test")
