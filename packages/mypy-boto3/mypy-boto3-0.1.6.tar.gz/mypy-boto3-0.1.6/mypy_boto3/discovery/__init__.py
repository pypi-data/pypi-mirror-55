try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_discovery_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_discovery import *
    except ImportError:
        raise ImportError("Install mypy_boto3[discovery] to use mypy_boto3.discovery")
