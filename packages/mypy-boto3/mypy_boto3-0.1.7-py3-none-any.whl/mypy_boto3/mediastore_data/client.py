try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_mediastore_data_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_mediastore_data.client import *  # type: ignore
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[mediastore-data] to use mypy_boto3.mediastore_data"
        )
