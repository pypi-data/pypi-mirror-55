import logging
import os


def init(padding=10, log_level_override=None):
    log_level = os.getenv("LOG_LEVEL", logging.INFO)
    if log_level_override is not None:
        log_level = log_level_override
    fmt = "%(asctime)s %(name)-{}s %(levelname)s: %(message)s".format(padding)
    if os.getenv("ENV") == "LOCAL":
        import coloredlogs

        coloredlogs.install(
            fmt="%(asctime)s,%(msecs)03d %(name)-{}s %(levelname)s: %(message)s".format(
                padding
            ),
            level=log_level,
        )
    else:
        root = logging.getLogger()
        if root.handlers:
            for handler in root.handlers:
                root.removeHandler(handler)
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s %(name)-{}s %(levelname)s: %(message)s".format(padding),
        )
