try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_backup_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_backup import *
    except ImportError:
        raise ImportError("Install mypy_boto3[backup] to use mypy_boto3.backup")
