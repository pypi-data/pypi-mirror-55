try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_elb_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_elb import *
    except ImportError:
        raise ImportError("Install mypy_boto3[elb] to use mypy_boto3.elb")
