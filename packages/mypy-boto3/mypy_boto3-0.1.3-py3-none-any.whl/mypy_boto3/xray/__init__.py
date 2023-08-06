try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_xray_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_xray import *
    except ImportError:
        raise ImportError("Install mypy_boto3[xray] to use mypy_boto3.xray")
