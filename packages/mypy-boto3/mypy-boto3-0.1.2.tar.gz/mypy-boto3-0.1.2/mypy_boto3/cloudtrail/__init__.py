try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_cloudtrail_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_cloudtrail import *
    except ImportError:
        raise ImportError("Install mypy_boto3[cloudtrail] to use mypy_boto3.cloudtrail")
