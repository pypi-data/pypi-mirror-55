try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_guardduty_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_guardduty.client import *
    except ImportError:
        raise ImportError("Install mypy_boto3[guardduty] to use mypy_boto3.guardduty")
