try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_support_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_support import *
    except ImportError:
        raise ImportError("Install mypy_boto3[support] to use mypy_boto3.support")
