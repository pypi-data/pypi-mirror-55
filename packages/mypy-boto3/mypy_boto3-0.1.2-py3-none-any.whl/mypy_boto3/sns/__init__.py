try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_sns_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_sns import *
    except ImportError:
        raise ImportError("Install mypy_boto3[sns] to use mypy_boto3.sns")
