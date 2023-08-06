try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_pinpoint_email_with_docs.paginator import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_pinpoint_email.paginator import *  # type: ignore
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[pinpoint-email] to use mypy_boto3.pinpoint_email"
        )
