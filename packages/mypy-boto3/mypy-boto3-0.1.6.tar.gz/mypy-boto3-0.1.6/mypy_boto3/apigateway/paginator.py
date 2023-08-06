try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_apigateway_with_docs.paginator import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_apigateway.paginator import *
    except ImportError:
        raise ImportError("Install mypy_boto3[apigateway] to use mypy_boto3.apigateway")
