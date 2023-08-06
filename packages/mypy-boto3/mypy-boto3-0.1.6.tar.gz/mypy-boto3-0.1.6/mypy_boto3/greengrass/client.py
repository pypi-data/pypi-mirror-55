try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_greengrass_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_greengrass.client import *
    except ImportError:
        raise ImportError("Install mypy_boto3[greengrass] to use mypy_boto3.greengrass")
