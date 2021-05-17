import io
import os
import subprocess
from asyncio.log import logger
import json
import pandas as pd

TABBY_JAVA_VERSION = "2.0.0"
JAR_NAME = "ispras_tbl_extr.jar".format(TABBY_JAVA_VERSION)
JAR_DIR = os.path.abspath(os.path.dirname(__file__))
JAVA_NOT_FOUND_ERROR = (
    "`java` command is not found from this Python process."
    "Please ensure Java is installed and PATH is set for `java`"
)

DEFAULT_CONFIG = {"JAR_PATH": os.path.join(JAR_DIR, JAR_NAME)}


class JavaNotFoundError:
    pass


def _jar_path():
    return os.environ.get("TABBY_JAR", DEFAULT_CONFIG["JAR_PATH"])


def _run(path=None, encoding="utf-8"):

    args = ["java"] + ["-jar", _jar_path(), "-i", "./"+path, "-o", "out"]

    try:
        result = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.DEVNULL,
            check=True,
        )
        if result.stderr:
            logger.warning("Got stderr: {}".format(result.stderr.decode(encoding)))
        return result.stdout
    except FileNotFoundError:
        raise JavaNotFoundError(JAVA_NOT_FOUND_ERROR)
    except subprocess.CalledProcessError as e:
        logger.error("Error from tabby-java:\n{}\n".format(e.stderr.decode(encoding)))
        raise


if __name__ == '__main__':
    output = _run('032.pdf')
    response = output.decode('UTF-8')
    pages = json.loads(response)
    print(pages["pages"])