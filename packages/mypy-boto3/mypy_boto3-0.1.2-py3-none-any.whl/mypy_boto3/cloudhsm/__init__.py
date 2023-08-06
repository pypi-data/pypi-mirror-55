try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_cloudhsm_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_cloudhsm import *
    except ImportError:
        raise ImportError("Install mypy_boto3[cloudhsm] to use mypy_boto3.cloudhsm")
