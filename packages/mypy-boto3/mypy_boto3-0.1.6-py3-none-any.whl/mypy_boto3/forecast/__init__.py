try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_forecast_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_forecast import *
    except ImportError:
        raise ImportError("Install mypy_boto3[forecast] to use mypy_boto3.forecast")
