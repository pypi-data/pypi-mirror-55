try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_elastictranscoder_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_elastictranscoder import *  # type: ignore
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[elastictranscoder] to use mypy_boto3.elastictranscoder"
        )
