try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_ssm_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_ssm import *
    except ImportError:
        raise ImportError("Install mypy_boto3[ssm] to use mypy_boto3.ssm")
