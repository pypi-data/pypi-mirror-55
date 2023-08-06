try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_sms_with_docs.paginator import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_sms.paginator import *  # type: ignore
    except ImportError:
        raise ImportError("Install mypy_boto3[sms] to use mypy_boto3.sms")
