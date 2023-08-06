try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_iot_data_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_iot_data.client import *
    except ImportError:
        raise ImportError("Install mypy_boto3[iot-data] to use mypy_boto3.iot_data")
