try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_firehose_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_firehose import *
    except ImportError:
        raise ImportError("Install mypy_boto3[firehose] to use mypy_boto3.firehose")
