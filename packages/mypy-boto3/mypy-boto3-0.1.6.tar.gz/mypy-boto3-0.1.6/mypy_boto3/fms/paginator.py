try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_fms_with_docs.paginator import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_fms.paginator import *
    except ImportError:
        raise ImportError("Install mypy_boto3[fms] to use mypy_boto3.fms")
