try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_organizations_with_docs.paginator import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_organizations.paginator import *  # type: ignore
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[organizations] to use mypy_boto3.organizations"
        )
