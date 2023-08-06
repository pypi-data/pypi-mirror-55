try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_shield_with_docs.paginator import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_shield.paginator import *
    except ImportError:
        raise ImportError("Install mypy_boto3[shield] to use mypy_boto3.shield")
