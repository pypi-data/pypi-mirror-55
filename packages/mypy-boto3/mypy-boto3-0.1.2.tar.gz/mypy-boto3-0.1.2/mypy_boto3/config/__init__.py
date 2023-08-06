try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_config_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_config import *
    except ImportError:
        raise ImportError("Install mypy_boto3[config] to use mypy_boto3.config")
