try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_managedblockchain_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_managedblockchain.client import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[managedblockchain] to use mypy_boto3.managedblockchain"
        )
