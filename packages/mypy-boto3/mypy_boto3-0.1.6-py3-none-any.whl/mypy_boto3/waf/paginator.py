try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_waf_with_docs.paginator import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_waf.paginator import *
    except ImportError:
        raise ImportError("Install mypy_boto3[waf] to use mypy_boto3.waf")
