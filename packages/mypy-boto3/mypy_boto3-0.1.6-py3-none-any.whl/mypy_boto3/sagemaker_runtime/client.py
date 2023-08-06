try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_sagemaker_runtime_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_sagemaker_runtime.client import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[sagemaker-runtime] to use mypy_boto3.sagemaker_runtime"
        )
