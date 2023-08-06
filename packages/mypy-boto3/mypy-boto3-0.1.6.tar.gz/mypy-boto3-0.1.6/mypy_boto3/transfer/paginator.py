try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_transfer_with_docs.paginator import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_transfer.paginator import *
    except ImportError:
        raise ImportError("Install mypy_boto3[transfer] to use mypy_boto3.transfer")
