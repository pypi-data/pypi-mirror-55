try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_transcribe_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_transcribe.client import *
    except ImportError:
        raise ImportError("Install mypy_boto3[transcribe] to use mypy_boto3.transcribe")
