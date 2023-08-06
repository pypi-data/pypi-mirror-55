try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_chime_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_chime import *
    except ImportError:
        raise ImportError("Install mypy_boto3[chime] to use mypy_boto3.chime")
