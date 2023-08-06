try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_elasticache_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_elasticache.client import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[elasticache] to use mypy_boto3.elasticache"
        )
