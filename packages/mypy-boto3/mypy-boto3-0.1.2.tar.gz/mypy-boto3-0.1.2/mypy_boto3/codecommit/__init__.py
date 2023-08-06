try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_codecommit_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_codecommit import *
    except ImportError:
        raise ImportError("Install mypy_boto3[codecommit] to use mypy_boto3.codecommit")
