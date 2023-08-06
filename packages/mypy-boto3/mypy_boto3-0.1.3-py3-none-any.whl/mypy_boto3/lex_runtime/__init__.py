try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_lex_runtime_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_lex_runtime import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[lex-runtime] to use mypy_boto3.lex_runtime"
        )
