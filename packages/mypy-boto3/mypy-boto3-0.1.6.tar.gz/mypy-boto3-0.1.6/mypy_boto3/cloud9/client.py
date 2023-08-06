try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_cloud9_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_cloud9.client import *
    except ImportError:
        raise ImportError("Install mypy_boto3[cloud9] to use mypy_boto3.cloud9")
