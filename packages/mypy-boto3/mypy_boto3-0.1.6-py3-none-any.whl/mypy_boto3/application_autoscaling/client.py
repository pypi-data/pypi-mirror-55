try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_application_autoscaling_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_application_autoscaling.client import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[application-autoscaling] to use mypy_boto3.application_autoscaling"
        )
