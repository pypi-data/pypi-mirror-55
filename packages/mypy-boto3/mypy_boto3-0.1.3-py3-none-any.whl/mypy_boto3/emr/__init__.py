try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_emr_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_emr import *
    except ImportError:
        raise ImportError("Install mypy_boto3[emr] to use mypy_boto3.emr")
