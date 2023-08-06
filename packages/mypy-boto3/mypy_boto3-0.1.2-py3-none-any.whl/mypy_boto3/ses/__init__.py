try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_ses_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_ses import *
    except ImportError:
        raise ImportError("Install mypy_boto3[ses] to use mypy_boto3.ses")
