try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_workmail_with_docs.paginator import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_workmail.paginator import *
    except ImportError:
        raise ImportError("Install mypy_boto3[workmail] to use mypy_boto3.workmail")
