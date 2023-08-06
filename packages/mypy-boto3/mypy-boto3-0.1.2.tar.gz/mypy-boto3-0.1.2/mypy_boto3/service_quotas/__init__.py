try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_service_quotas_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_service_quotas import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[service-quotas] to use mypy_boto3.service_quotas"
        )
