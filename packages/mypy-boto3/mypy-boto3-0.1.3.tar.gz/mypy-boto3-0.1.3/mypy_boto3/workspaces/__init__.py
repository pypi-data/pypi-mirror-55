try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_workspaces_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_workspaces import *
    except ImportError:
        raise ImportError("Install mypy_boto3[workspaces] to use mypy_boto3.workspaces")
