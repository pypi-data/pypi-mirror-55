try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_mediastore_with_docs.paginator import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_mediastore.paginator import *  # type: ignore
    except ImportError:
        raise ImportError("Install mypy_boto3[mediastore] to use mypy_boto3.mediastore")
