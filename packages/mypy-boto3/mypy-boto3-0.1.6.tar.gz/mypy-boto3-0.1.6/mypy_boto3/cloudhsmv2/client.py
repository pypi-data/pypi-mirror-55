try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_cloudhsmv2_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_cloudhsmv2.client import *
    except ImportError:
        raise ImportError("Install mypy_boto3[cloudhsmv2] to use mypy_boto3.cloudhsmv2")
