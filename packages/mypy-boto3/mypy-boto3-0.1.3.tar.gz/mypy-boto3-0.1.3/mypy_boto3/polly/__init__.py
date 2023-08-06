try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_polly_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_polly import *
    except ImportError:
        raise ImportError("Install mypy_boto3[polly] to use mypy_boto3.polly")
