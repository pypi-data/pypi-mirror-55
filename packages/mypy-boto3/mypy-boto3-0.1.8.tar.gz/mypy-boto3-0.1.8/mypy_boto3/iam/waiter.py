try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_iam_with_docs.waiter import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_iam.waiter import *  # type: ignore
    except ImportError:
        raise ImportError("Install mypy_boto3[iam] to use mypy_boto3.iam")
