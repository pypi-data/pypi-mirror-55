try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_rekognition_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_rekognition import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[rekognition] to use mypy_boto3.rekognition"
        )
