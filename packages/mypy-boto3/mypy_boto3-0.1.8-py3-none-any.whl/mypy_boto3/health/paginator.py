try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_health_with_docs.paginator import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_health.paginator import *  # type: ignore
    except ImportError:
        raise ImportError("Install mypy_boto3[health] to use mypy_boto3.health")
