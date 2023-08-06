try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_snowball_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_snowball.client import *  # type: ignore
    except ImportError:
        raise ImportError("Install mypy_boto3[snowball] to use mypy_boto3.snowball")
