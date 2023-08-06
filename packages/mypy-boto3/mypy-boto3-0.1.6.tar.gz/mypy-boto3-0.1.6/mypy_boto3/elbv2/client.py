try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_elbv2_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_elbv2.client import *
    except ImportError:
        raise ImportError("Install mypy_boto3[elbv2] to use mypy_boto3.elbv2")
