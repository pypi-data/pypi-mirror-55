try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_comprehendmedical_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_comprehendmedical.client import *  # type: ignore
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[comprehendmedical] to use mypy_boto3.comprehendmedical"
        )
