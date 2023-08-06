try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_glue_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_glue import *
    except ImportError:
        raise ImportError("Install mypy_boto3[glue] to use mypy_boto3.glue")
