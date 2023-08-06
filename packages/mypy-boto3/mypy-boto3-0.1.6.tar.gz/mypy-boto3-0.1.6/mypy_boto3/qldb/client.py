try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_qldb_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_qldb.client import *
    except ImportError:
        raise ImportError("Install mypy_boto3[qldb] to use mypy_boto3.qldb")
