try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_codebuild_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_codebuild import *
    except ImportError:
        raise ImportError("Install mypy_boto3[codebuild] to use mypy_boto3.codebuild")
