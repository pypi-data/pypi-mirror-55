try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_ds_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_ds.client import *
    except ImportError:
        raise ImportError("Install mypy_boto3[ds] to use mypy_boto3.ds")
