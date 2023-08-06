try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_opsworkscm_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_opsworkscm import *
    except ImportError:
        raise ImportError("Install mypy_boto3[opsworkscm] to use mypy_boto3.opsworkscm")
