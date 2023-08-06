try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_stepfunctions_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_stepfunctions import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[stepfunctions] to use mypy_boto3.stepfunctions"
        )
