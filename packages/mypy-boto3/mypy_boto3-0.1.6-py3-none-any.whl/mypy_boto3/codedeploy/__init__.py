try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_codedeploy_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_codedeploy import *
    except ImportError:
        raise ImportError("Install mypy_boto3[codedeploy] to use mypy_boto3.codedeploy")
