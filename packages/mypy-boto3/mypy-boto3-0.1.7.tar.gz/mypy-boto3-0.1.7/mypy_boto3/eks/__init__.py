try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_eks_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_eks import *  # type: ignore
    except ImportError:
        raise ImportError("Install mypy_boto3[eks] to use mypy_boto3.eks")
