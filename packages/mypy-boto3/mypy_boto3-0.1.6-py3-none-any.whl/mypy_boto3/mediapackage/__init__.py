try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_mediapackage_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_mediapackage import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[mediapackage] to use mypy_boto3.mediapackage"
        )
