try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_route53resolver_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_route53resolver.client import *  # type: ignore
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[route53resolver] to use mypy_boto3.route53resolver"
        )
