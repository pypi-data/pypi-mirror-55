try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_mediapackage_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_mediapackage.client import *  # type: ignore
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[mediapackage] to use mypy_boto3.mediapackage"
        )
