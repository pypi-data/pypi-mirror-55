try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_ecr_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_ecr import *
    except ImportError:
        raise ImportError("Install mypy_boto3[ecr] to use mypy_boto3.ecr")
