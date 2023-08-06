try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_forecastquery_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_forecastquery import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[forecastquery] to use mypy_boto3.forecastquery"
        )
