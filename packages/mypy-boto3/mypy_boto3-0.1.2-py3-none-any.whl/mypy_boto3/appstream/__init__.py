try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_appstream_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_appstream import *
    except ImportError:
        raise ImportError("Install mypy_boto3[appstream] to use mypy_boto3.appstream")
