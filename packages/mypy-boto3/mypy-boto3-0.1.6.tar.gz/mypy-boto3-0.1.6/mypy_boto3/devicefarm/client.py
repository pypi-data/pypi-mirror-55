try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_devicefarm_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_devicefarm.client import *
    except ImportError:
        raise ImportError("Install mypy_boto3[devicefarm] to use mypy_boto3.devicefarm")
