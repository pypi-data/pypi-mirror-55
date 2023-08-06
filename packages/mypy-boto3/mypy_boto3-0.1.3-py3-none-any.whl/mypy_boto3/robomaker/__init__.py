try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_robomaker_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_robomaker import *
    except ImportError:
        raise ImportError("Install mypy_boto3[robomaker] to use mypy_boto3.robomaker")
