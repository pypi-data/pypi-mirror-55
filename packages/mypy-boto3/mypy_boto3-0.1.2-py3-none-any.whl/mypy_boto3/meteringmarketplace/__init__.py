try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_meteringmarketplace_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_meteringmarketplace import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[meteringmarketplace] to use mypy_boto3.meteringmarketplace"
        )
