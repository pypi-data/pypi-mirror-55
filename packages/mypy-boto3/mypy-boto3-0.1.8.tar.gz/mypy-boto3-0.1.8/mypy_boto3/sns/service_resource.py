try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_sns_with_docs.service_resource import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_sns.service_resource import *  # type: ignore
    except ImportError:
        raise ImportError("Install mypy_boto3[sns] to use mypy_boto3.sns")
