try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_s3_with_docs.paginator import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_s3.paginator import *
    except ImportError:
        raise ImportError("Install mypy_boto3[s3] to use mypy_boto3.s3")
