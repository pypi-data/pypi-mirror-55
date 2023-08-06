try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_iotevents_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_iotevents.client import *
    except ImportError:
        raise ImportError("Install mypy_boto3[iotevents] to use mypy_boto3.iotevents")
