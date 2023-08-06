try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_mediapackage_vod_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_mediapackage_vod import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[mediapackage-vod] to use mypy_boto3.mediapackage_vod"
        )
