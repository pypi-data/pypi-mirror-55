try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_devicefarm_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_devicefarm import *
    except ImportError:
        raise ImportError("Install mypy_boto3[devicefarm] to use mypy_boto3.devicefarm")
