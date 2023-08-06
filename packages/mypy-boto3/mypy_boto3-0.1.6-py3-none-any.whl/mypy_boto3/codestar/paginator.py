try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_codestar_with_docs.paginator import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_codestar.paginator import *
    except ImportError:
        raise ImportError("Install mypy_boto3[codestar] to use mypy_boto3.codestar")
