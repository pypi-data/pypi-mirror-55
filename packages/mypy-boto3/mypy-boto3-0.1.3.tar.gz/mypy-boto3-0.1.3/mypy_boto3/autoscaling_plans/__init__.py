try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_autoscaling_plans_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_autoscaling_plans import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[autoscaling-plans] to use mypy_boto3.autoscaling_plans"
        )
