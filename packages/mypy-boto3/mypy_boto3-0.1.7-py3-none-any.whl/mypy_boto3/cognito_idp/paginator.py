try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_cognito_idp_with_docs.paginator import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_cognito_idp.paginator import *  # type: ignore
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[cognito-idp] to use mypy_boto3.cognito_idp"
        )
