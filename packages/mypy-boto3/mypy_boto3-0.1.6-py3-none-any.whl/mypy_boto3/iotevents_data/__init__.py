try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_iotevents_data_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_iotevents_data import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[iotevents-data] to use mypy_boto3.iotevents_data"
        )
