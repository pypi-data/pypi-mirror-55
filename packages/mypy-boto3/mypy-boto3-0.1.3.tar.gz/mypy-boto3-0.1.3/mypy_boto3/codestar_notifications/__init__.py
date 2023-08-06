try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_codestar_notifications_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_codestar_notifications import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[codestar-notifications] to use mypy_boto3.codestar_notifications"
        )
