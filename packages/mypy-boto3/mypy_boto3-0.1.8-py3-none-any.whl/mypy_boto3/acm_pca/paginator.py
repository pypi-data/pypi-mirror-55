try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_acm_pca_with_docs.paginator import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_acm_pca.paginator import *  # type: ignore
    except ImportError:
        raise ImportError("Install mypy_boto3[acm-pca] to use mypy_boto3.acm_pca")
