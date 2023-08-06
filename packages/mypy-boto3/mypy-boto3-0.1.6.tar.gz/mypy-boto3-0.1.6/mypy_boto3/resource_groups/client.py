try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_resource_groups_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_resource_groups.client import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[resource-groups] to use mypy_boto3.resource_groups"
        )
