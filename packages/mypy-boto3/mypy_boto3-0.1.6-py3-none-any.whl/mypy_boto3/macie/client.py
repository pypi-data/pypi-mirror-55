try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_macie_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_macie.client import *
    except ImportError:
        raise ImportError("Install mypy_boto3[macie] to use mypy_boto3.macie")
