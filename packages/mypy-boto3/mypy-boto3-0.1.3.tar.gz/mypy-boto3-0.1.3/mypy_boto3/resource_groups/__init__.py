try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_resource_groups_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_resource_groups import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[resource-groups] to use mypy_boto3.resource_groups"
        )
