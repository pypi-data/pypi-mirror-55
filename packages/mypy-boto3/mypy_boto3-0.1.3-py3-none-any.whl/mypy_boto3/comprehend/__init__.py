try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_comprehend_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_comprehend import *
    except ImportError:
        raise ImportError("Install mypy_boto3[comprehend] to use mypy_boto3.comprehend")
