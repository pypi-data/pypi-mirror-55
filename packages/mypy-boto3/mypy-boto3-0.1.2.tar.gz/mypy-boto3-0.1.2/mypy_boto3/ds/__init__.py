try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_ds_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_ds import *
    except ImportError:
        raise ImportError("Install mypy_boto3[ds] to use mypy_boto3.ds")
