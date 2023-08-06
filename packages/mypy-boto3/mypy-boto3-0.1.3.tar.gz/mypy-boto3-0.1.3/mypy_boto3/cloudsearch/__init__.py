try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_cloudsearch_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_cloudsearch import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[cloudsearch] to use mypy_boto3.cloudsearch"
        )
