try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_glacier_with_docs.service_resource import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_glacier.service_resource import *
    except ImportError:
        raise ImportError("Install mypy_boto3[glacier] to use mypy_boto3.glacier")
