try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_globalaccelerator_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_globalaccelerator import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[globalaccelerator] to use mypy_boto3.globalaccelerator"
        )
