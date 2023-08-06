try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_serverlessrepo_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_serverlessrepo import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[serverlessrepo] to use mypy_boto3.serverlessrepo"
        )
