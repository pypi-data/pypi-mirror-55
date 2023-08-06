try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_opsworks_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_opsworks import *
    except ImportError:
        raise ImportError("Install mypy_boto3[opsworks] to use mypy_boto3.opsworks")
