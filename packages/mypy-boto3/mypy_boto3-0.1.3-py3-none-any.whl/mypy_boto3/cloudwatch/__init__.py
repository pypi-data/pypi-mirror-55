try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_cloudwatch_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_cloudwatch import *
    except ImportError:
        raise ImportError("Install mypy_boto3[cloudwatch] to use mypy_boto3.cloudwatch")
