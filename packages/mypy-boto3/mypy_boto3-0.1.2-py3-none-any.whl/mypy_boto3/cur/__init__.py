try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_cur_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_cur import *
    except ImportError:
        raise ImportError("Install mypy_boto3[cur] to use mypy_boto3.cur")
