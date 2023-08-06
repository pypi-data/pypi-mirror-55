try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_kinesis_video_media_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_kinesis_video_media import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[kinesis-video-media] to use mypy_boto3.kinesis_video_media"
        )
