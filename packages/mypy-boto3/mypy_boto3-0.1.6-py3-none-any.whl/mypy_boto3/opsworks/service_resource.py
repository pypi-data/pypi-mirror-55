try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_opsworks_with_docs.service_resource import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_opsworks.service_resource import *
    except ImportError:
        raise ImportError("Install mypy_boto3[opsworks] to use mypy_boto3.opsworks")
