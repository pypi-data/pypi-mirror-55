try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_dax_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_dax import *
    except ImportError:
        raise ImportError("Install mypy_boto3[dax] to use mypy_boto3.dax")
