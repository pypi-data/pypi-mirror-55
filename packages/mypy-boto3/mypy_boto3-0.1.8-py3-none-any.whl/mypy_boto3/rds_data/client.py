try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_rds_data_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_rds_data.client import *  # type: ignore
    except ImportError:
        raise ImportError("Install mypy_boto3[rds-data] to use mypy_boto3.rds_data")
