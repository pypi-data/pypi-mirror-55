try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_cloudsearchdomain_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_cloudsearchdomain import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[cloudsearchdomain] to use mypy_boto3.cloudsearchdomain"
        )
