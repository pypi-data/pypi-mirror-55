try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_iotanalytics_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_iotanalytics import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[iotanalytics] to use mypy_boto3.iotanalytics"
        )
