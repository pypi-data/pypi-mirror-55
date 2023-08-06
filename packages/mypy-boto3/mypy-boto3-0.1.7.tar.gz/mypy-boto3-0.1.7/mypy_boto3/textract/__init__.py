try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_textract_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_textract import *  # type: ignore
    except ImportError:
        raise ImportError("Install mypy_boto3[textract] to use mypy_boto3.textract")
