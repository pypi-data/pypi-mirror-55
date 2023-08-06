try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_kms_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_kms import *
    except ImportError:
        raise ImportError("Install mypy_boto3[kms] to use mypy_boto3.kms")
