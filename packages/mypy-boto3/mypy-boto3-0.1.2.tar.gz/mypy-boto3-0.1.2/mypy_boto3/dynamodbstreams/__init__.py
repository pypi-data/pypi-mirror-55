try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_dynamodbstreams_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_dynamodbstreams import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[dynamodbstreams] to use mypy_boto3.dynamodbstreams"
        )
