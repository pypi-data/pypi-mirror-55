try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_iot1click_devices_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_iot1click_devices import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[iot1click-devices] to use mypy_boto3.iot1click_devices"
        )
