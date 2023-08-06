try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_iotthingsgraph_with_docs.paginator import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_iotthingsgraph.paginator import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[iotthingsgraph] to use mypy_boto3.iotthingsgraph"
        )
