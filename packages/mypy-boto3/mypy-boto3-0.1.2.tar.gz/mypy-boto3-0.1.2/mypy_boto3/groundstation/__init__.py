try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_groundstation_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_groundstation import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[groundstation] to use mypy_boto3.groundstation"
        )
