try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_cognito_identity_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_cognito_identity.client import *  # type: ignore
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[cognito-identity] to use mypy_boto3.cognito_identity"
        )
