try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_comprehendmedical_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_comprehendmedical import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[comprehendmedical] to use mypy_boto3.comprehendmedical"
        )
