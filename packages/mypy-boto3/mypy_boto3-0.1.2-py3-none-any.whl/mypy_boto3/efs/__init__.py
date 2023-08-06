try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_efs_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_efs import *
    except ImportError:
        raise ImportError("Install mypy_boto3[efs] to use mypy_boto3.efs")
