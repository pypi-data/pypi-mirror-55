try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_rds_with_docs.paginator import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_rds.paginator import *
    except ImportError:
        raise ImportError("Install mypy_boto3[rds] to use mypy_boto3.rds")
