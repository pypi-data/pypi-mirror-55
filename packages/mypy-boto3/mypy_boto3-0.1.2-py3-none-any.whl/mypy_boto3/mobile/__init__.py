try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_mobile_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_mobile import *
    except ImportError:
        raise ImportError("Install mypy_boto3[mobile] to use mypy_boto3.mobile")
