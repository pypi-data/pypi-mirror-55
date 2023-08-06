try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_workmailmessageflow_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_workmailmessageflow.client import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[workmailmessageflow] to use mypy_boto3.workmailmessageflow"
        )
