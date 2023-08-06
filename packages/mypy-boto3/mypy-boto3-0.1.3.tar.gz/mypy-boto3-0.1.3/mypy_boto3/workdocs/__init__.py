try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_workdocs_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_workdocs import *
    except ImportError:
        raise ImportError("Install mypy_boto3[workdocs] to use mypy_boto3.workdocs")
