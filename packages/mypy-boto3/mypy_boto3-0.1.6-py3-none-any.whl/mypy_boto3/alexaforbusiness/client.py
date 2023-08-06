try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_alexaforbusiness_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_alexaforbusiness.client import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[alexaforbusiness] to use mypy_boto3.alexaforbusiness"
        )
