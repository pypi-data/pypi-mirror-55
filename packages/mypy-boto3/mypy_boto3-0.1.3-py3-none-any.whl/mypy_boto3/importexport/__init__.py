try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_importexport_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_importexport import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[importexport] to use mypy_boto3.importexport"
        )
