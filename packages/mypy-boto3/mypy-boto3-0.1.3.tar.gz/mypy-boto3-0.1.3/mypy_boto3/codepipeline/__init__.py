try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_codepipeline_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_codepipeline import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[codepipeline] to use mypy_boto3.codepipeline"
        )
