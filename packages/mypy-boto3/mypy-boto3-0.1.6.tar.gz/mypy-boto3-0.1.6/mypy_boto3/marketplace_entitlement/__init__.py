try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_marketplace_entitlement_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_marketplace_entitlement import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[marketplace-entitlement] to use mypy_boto3.marketplace_entitlement"
        )
