try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_application_insights_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_application_insights import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[application-insights] to use mypy_boto3.application_insights"
        )
