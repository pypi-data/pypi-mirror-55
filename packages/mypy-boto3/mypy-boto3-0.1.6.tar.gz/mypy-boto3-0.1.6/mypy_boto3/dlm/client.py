try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_dlm_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_dlm.client import *
    except ImportError:
        raise ImportError("Install mypy_boto3[dlm] to use mypy_boto3.dlm")
