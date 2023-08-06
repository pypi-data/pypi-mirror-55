try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_logs_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_logs.client import *  # type: ignore
    except ImportError:
        raise ImportError("Install mypy_boto3[logs] to use mypy_boto3.logs")
