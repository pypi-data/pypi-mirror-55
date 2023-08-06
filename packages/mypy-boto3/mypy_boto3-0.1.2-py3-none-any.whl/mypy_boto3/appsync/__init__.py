try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_appsync_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_appsync import *
    except ImportError:
        raise ImportError("Install mypy_boto3[appsync] to use mypy_boto3.appsync")
