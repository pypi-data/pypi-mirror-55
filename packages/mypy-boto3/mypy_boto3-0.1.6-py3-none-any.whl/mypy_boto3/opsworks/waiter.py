try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_opsworks_with_docs.waiter import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_opsworks.waiter import *
    except ImportError:
        raise ImportError("Install mypy_boto3[opsworks] to use mypy_boto3.opsworks")
