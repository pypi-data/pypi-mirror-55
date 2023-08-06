try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_acm_with_docs.paginator import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_acm.paginator import *
    except ImportError:
        raise ImportError("Install mypy_boto3[acm] to use mypy_boto3.acm")
