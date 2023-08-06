try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_kinesisanalytics_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_kinesisanalytics import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[kinesisanalytics] to use mypy_boto3.kinesisanalytics"
        )
