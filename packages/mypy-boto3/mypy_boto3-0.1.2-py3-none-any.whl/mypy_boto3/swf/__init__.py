try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_swf_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_swf import *
    except ImportError:
        raise ImportError("Install mypy_boto3[swf] to use mypy_boto3.swf")
