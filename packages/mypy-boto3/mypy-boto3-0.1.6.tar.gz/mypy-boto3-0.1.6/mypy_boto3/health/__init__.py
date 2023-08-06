try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_health_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_health import *
    except ImportError:
        raise ImportError("Install mypy_boto3[health] to use mypy_boto3.health")
