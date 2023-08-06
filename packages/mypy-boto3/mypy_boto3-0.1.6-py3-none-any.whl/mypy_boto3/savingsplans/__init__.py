try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_savingsplans_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_savingsplans import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[savingsplans] to use mypy_boto3.savingsplans"
        )
