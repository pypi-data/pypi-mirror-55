try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_route53domains_with_docs.paginator import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_route53domains.paginator import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[route53domains] to use mypy_boto3.route53domains"
        )
