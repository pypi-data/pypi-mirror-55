try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_pinpoint_email_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_pinpoint_email import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[pinpoint-email] to use mypy_boto3.pinpoint_email"
        )
