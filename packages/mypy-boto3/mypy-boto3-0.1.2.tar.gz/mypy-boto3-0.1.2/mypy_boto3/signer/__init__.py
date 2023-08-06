try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_signer_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_signer import *
    except ImportError:
        raise ImportError("Install mypy_boto3[signer] to use mypy_boto3.signer")
