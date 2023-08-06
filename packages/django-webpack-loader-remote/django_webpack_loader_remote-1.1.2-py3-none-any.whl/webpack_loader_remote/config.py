import re

from django.conf import settings


__all__ = ("load_config",)


DEFAULT_CONFIG = {
    "DEFAULT": {
        "CACHE": not settings.DEBUG,
        "BUNDLE_DIR_NAME": "webpack_bundles/",
        "STATS_FILE": "webpack-stats.json",
        "STATS_FILE_TIMEOUT": 3.0,
        "STATS_FILE_SECRET_KEY": "THIS_IS_A_REALLY_SECRET_KEY",
        "STATS_FILE_SECRET_KEY_HEADER_NAME": "Secret-Key",
        "AWS_ACCESS_KEY": settings.AWS_ACCESS_KEY_ID,
        "AWS_SECRET_KEY": settings.AWS_SECRET_ACCESS_KEY,
        "POLL_INTERVAL": 0.1,
        "TIMEOUT": None,
        "IGNORE": [r".+\.hot-update.js", r".+\.map"],
    }
}

user_config = getattr(settings, "WEBPACK_LOADER_REMOTE", DEFAULT_CONFIG)

user_config = dict(
    (name, dict(DEFAULT_CONFIG["DEFAULT"], **cfg)) for name, cfg in user_config.items()
)

for entry in user_config.values():
    entry["ignores"] = [re.compile(I) for I in entry["IGNORE"]]


def load_config(name):
    return user_config[name]
