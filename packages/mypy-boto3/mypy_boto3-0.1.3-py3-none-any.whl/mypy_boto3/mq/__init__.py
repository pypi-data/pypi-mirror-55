try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_mq_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_mq import *
    except ImportError:
        raise ImportError("Install mypy_boto3[mq] to use mypy_boto3.mq")
