try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_apigatewaymanagementapi_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_apigatewaymanagementapi import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[apigatewaymanagementapi] to use mypy_boto3.apigatewaymanagementapi"
        )
