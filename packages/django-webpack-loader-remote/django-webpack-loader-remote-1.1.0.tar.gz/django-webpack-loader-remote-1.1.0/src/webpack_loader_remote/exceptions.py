__all__ = (
    "WebpackError",
    "WebpackLoaderRemoteBadStatsError",
    "WebpackLoaderRemoteTimeoutError",
    "WebpackBundleLookupError",
)


class BaseWebpackLoaderRemoteException(Exception):
    """
    Base exception for django-webpack-loader-remote.
    """


class WebpackError(BaseWebpackLoaderRemoteException):
    """
    General webpack loader error.
    """


class WebpackLoaderRemoteBadStatsError(BaseWebpackLoaderRemoteException):
    """
    The stats file does not contain valid data.
    """


class WebpackLoaderRemoteTimeoutError(BaseWebpackLoaderRemoteException):
    """
    The bundle took too long to compile.
    """


class WebpackBundleLookupError(BaseWebpackLoaderRemoteException):
    """
    The bundle name was invalid.
    """
