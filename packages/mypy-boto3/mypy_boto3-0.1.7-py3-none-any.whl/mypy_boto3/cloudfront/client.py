try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_cloudfront_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_cloudfront.client import *  # type: ignore
    except ImportError:
        raise ImportError("Install mypy_boto3[cloudfront] to use mypy_boto3.cloudfront")
