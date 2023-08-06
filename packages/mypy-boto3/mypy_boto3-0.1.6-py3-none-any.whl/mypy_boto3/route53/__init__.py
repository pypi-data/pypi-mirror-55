try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_route53_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_route53 import *
    except ImportError:
        raise ImportError("Install mypy_boto3[route53] to use mypy_boto3.route53")
