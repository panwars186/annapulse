import logging
import sys


def setup_logging(level: int = logging.INFO) -> None:
    """
    Configure application-wide logging.

    This should be called once at startup before the app begins handling requests.
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

