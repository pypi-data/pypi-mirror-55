try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_sqs_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_sqs import *
    except ImportError:
        raise ImportError("Install mypy_boto3[sqs] to use mypy_boto3.sqs")
