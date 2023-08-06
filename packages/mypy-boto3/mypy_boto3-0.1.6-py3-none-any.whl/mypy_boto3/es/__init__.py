try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_es_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_es import *
    except ImportError:
        raise ImportError("Install mypy_boto3[es] to use mypy_boto3.es")
