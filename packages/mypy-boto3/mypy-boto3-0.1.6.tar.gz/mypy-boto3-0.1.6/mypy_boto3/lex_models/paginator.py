try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_lex_models_with_docs.paginator import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_lex_models.paginator import *
    except ImportError:
        raise ImportError("Install mypy_boto3[lex-models] to use mypy_boto3.lex_models")
