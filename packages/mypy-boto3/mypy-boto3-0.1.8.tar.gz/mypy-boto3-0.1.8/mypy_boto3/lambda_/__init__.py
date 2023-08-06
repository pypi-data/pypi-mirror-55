try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_lambda_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_lambda import *  # type: ignore
    except ImportError:
        raise ImportError("Install mypy_boto3[lambda] to use mypy_boto3.lambda_")
