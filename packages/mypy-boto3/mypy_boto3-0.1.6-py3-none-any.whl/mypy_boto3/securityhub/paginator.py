try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_securityhub_with_docs.paginator import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_securityhub.paginator import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[securityhub] to use mypy_boto3.securityhub"
        )
