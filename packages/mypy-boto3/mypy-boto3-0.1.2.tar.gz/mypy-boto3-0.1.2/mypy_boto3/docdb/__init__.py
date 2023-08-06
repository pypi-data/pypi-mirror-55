try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_docdb_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_docdb import *
    except ImportError:
        raise ImportError("Install mypy_boto3[docdb] to use mypy_boto3.docdb")
