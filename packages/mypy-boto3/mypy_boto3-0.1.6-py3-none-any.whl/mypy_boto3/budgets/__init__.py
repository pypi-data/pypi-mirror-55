try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_budgets_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_budgets import *
    except ImportError:
        raise ImportError("Install mypy_boto3[budgets] to use mypy_boto3.budgets")
