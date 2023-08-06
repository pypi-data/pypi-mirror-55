try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_kinesisanalyticsv2_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_kinesisanalyticsv2 import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[kinesisanalyticsv2] to use mypy_boto3.kinesisanalyticsv2"
        )
