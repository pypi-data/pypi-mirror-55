try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_qldb_session_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_qldb_session import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[qldb-session] to use mypy_boto3.qldb_session"
        )
