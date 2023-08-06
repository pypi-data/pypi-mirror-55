try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_autoscaling_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_autoscaling import *  # type: ignore
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[autoscaling] to use mypy_boto3.autoscaling"
        )
