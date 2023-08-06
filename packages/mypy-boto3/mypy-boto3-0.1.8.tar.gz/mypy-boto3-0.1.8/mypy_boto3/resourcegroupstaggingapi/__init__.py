try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_resourcegroupstaggingapi_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_resourcegroupstaggingapi import *  # type: ignore
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[resourcegroupstaggingapi] to use mypy_boto3.resourcegroupstaggingapi"
        )
