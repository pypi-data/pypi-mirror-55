try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_workmail_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_workmail import *
    except ImportError:
        raise ImportError("Install mypy_boto3[workmail] to use mypy_boto3.workmail")
