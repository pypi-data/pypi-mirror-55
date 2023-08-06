try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_resourcegroupstaggingapi_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_resourcegroupstaggingapi.client import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[resourcegroupstaggingapi] to use mypy_boto3.resourcegroupstaggingapi"
        )
