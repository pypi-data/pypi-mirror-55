try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_batch_with_docs.paginator import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_batch.paginator import *  # type: ignore
    except ImportError:
        raise ImportError("Install mypy_boto3[batch] to use mypy_boto3.batch")
