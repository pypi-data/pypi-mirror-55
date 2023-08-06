try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_servicediscovery_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_servicediscovery import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[servicediscovery] to use mypy_boto3.servicediscovery"
        )
