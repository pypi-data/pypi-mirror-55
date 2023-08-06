try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_inspector_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_inspector import *
    except ImportError:
        raise ImportError("Install mypy_boto3[inspector] to use mypy_boto3.inspector")
