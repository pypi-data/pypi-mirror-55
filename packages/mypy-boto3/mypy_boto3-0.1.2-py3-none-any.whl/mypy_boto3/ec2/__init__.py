try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_ec2_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_ec2 import *
    except ImportError:
        raise ImportError("Install mypy_boto3[ec2] to use mypy_boto3.ec2")
