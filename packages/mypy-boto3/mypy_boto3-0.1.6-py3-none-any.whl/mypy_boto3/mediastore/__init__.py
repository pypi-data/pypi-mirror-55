try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_mediastore_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_mediastore import *
    except ImportError:
        raise ImportError("Install mypy_boto3[mediastore] to use mypy_boto3.mediastore")
