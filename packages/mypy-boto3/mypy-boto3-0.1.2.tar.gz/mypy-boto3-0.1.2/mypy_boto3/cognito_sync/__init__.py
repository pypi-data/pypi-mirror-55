try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_cognito_sync_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_cognito_sync import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[cognito-sync] to use mypy_boto3.cognito_sync"
        )
