try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_worklink_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_worklink import *
    except ImportError:
        raise ImportError("Install mypy_boto3[worklink] to use mypy_boto3.worklink")
