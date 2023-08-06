try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_directconnect_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_directconnect import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[directconnect] to use mypy_boto3.directconnect"
        )
