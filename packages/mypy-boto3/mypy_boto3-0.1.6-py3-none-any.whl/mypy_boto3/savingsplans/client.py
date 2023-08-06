try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_savingsplans_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_savingsplans.client import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[savingsplans] to use mypy_boto3.savingsplans"
        )
