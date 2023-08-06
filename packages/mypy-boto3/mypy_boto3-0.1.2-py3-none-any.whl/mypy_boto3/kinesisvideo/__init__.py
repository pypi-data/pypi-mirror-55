try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_kinesisvideo_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_kinesisvideo import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[kinesisvideo] to use mypy_boto3.kinesisvideo"
        )
