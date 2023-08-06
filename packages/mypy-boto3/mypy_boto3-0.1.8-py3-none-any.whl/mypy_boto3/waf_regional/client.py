try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_waf_regional_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_waf_regional.client import *  # type: ignore
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[waf-regional] to use mypy_boto3.waf_regional"
        )
