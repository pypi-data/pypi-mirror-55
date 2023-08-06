try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_dynamodb_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_dynamodb import *
    except ImportError:
        raise ImportError("Install mypy_boto3[dynamodb] to use mypy_boto3.dynamodb")
