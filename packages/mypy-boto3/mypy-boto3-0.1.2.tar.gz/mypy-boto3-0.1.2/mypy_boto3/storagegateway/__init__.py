try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_storagegateway_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_storagegateway import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[storagegateway] to use mypy_boto3.storagegateway"
        )
