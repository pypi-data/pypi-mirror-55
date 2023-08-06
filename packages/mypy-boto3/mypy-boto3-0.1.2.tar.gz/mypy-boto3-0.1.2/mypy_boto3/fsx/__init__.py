try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_fsx_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_fsx import *
    except ImportError:
        raise ImportError("Install mypy_boto3[fsx] to use mypy_boto3.fsx")
