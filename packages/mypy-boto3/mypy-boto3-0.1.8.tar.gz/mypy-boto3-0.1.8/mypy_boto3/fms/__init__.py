try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_fms_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_fms import *  # type: ignore
    except ImportError:
        raise ImportError("Install mypy_boto3[fms] to use mypy_boto3.fms")
