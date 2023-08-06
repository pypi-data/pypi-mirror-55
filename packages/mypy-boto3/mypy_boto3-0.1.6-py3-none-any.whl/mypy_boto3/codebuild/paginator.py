try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_codebuild_with_docs.paginator import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_codebuild.paginator import *
    except ImportError:
        raise ImportError("Install mypy_boto3[codebuild] to use mypy_boto3.codebuild")
