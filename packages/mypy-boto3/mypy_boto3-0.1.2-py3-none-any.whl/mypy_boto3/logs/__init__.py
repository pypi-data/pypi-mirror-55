try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_logs_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_logs import *
    except ImportError:
        raise ImportError("Install mypy_boto3[logs] to use mypy_boto3.logs")
