try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_marketplacecommerceanalytics_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_marketplacecommerceanalytics import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[marketplacecommerceanalytics] to use mypy_boto3.marketplacecommerceanalytics"
        )
