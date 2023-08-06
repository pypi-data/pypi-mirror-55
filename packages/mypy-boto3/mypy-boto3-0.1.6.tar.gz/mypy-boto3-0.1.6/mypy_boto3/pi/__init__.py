try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_pi_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_pi import *
    except ImportError:
        raise ImportError("Install mypy_boto3[pi] to use mypy_boto3.pi")
