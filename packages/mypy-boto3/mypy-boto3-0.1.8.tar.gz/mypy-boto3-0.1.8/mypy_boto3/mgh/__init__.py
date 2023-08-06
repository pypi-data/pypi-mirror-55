try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_mgh_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_mgh import *  # type: ignore
    except ImportError:
        raise ImportError("Install mypy_boto3[mgh] to use mypy_boto3.mgh")
