try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_iot_with_docs.paginator import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_iot.paginator import *  # type: ignore
    except ImportError:
        raise ImportError("Install mypy_boto3[iot] to use mypy_boto3.iot")
