try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_s3control_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_s3control import *
    except ImportError:
        raise ImportError("Install mypy_boto3[s3control] to use mypy_boto3.s3control")
