try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_lakeformation_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_lakeformation import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[lakeformation] to use mypy_boto3.lakeformation"
        )
