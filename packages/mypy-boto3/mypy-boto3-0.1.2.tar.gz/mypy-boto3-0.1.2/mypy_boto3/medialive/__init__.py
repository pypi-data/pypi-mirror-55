try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_medialive_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_medialive import *
    except ImportError:
        raise ImportError("Install mypy_boto3[medialive] to use mypy_boto3.medialive")
