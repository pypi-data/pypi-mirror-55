try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_rds_data_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_rds_data import *
    except ImportError:
        raise ImportError("Install mypy_boto3[rds-data] to use mypy_boto3.rds_data")
