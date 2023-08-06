try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_mediatailor_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_mediatailor import *  # type: ignore
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[mediatailor] to use mypy_boto3.mediatailor"
        )
