try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_batch_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_batch import *
    except ImportError:
        raise ImportError("Install mypy_boto3[batch] to use mypy_boto3.batch")
