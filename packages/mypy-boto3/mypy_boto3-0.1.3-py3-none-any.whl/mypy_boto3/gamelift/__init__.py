try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_gamelift_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_gamelift import *
    except ImportError:
        raise ImportError("Install mypy_boto3[gamelift] to use mypy_boto3.gamelift")
