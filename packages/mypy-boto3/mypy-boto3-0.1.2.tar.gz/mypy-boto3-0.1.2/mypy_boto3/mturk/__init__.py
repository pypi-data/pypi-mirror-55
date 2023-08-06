try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_mturk_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_mturk import *
    except ImportError:
        raise ImportError("Install mypy_boto3[mturk] to use mypy_boto3.mturk")
