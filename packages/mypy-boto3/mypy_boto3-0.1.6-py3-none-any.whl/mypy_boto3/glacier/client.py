try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_glacier_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_glacier.client import *
    except ImportError:
        raise ImportError("Install mypy_boto3[glacier] to use mypy_boto3.glacier")
