try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_greengrass_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_greengrass import *  # type: ignore
    except ImportError:
        raise ImportError("Install mypy_boto3[greengrass] to use mypy_boto3.greengrass")
