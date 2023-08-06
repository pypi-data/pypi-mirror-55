try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_codebuild_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_codebuild.client import *
    except ImportError:
        raise ImportError("Install mypy_boto3[codebuild] to use mypy_boto3.codebuild")
