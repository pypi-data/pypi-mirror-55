try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_translate_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_translate import *
    except ImportError:
        raise ImportError("Install mypy_boto3[translate] to use mypy_boto3.translate")
