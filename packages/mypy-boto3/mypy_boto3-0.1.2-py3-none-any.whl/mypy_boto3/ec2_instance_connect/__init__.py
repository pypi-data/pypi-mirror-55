try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_ec2_instance_connect_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_ec2_instance_connect import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[ec2-instance-connect] to use mypy_boto3.ec2_instance_connect"
        )
