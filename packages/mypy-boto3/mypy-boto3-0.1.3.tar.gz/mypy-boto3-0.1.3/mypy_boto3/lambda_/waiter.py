try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_lambda__with_docs.waiter import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_lambda_.waiter import *
    except ImportError:
        raise ImportError("Install mypy_boto3[lambda] to use mypy_boto3.lambda_")
