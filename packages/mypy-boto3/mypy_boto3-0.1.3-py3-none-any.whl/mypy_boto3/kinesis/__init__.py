try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_kinesis_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_kinesis import *
    except ImportError:
        raise ImportError("Install mypy_boto3[kinesis] to use mypy_boto3.kinesis")
