try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_quicksight_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_quicksight.client import *
    except ImportError:
        raise ImportError("Install mypy_boto3[quicksight] to use mypy_boto3.quicksight")
