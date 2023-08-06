try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_athena_with_docs.paginator import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_athena.paginator import *  # type: ignore
    except ImportError:
        raise ImportError("Install mypy_boto3[athena] to use mypy_boto3.athena")
