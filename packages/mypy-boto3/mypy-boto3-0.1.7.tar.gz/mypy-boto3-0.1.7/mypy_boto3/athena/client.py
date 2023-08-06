try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_athena_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_athena.client import *  # type: ignore
    except ImportError:
        raise ImportError("Install mypy_boto3[athena] to use mypy_boto3.athena")
