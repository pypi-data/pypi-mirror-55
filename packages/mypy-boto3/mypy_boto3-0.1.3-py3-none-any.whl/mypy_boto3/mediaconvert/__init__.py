try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_mediaconvert_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_mediaconvert import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[mediaconvert] to use mypy_boto3.mediaconvert"
        )
