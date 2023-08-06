try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_license_manager_with_docs.paginator import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_license_manager.paginator import *  # type: ignore
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[license-manager] to use mypy_boto3.license_manager"
        )
