from django.core.checks import Error


BAD_CONFIG_ERROR = Error(
    "Error while parsing WEBPACK_LOADER_REMOTE configuration",
    hint="Is WEBPACK_LOADER_REMOTE config valid?",
    obj="django.conf.settings.WEBPACK_LOADER_REMOTE",
    id="django-webpack-loader-remote.E001",
)
