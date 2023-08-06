try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_securityhub_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_securityhub import *  # type: ignore
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[securityhub] to use mypy_boto3.securityhub"
        )
