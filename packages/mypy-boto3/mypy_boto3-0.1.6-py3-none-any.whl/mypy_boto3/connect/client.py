try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_connect_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_connect.client import *
    except ImportError:
        raise ImportError("Install mypy_boto3[connect] to use mypy_boto3.connect")
