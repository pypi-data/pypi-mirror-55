try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_dms_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_dms import *
    except ImportError:
        raise ImportError("Install mypy_boto3[dms] to use mypy_boto3.dms")
