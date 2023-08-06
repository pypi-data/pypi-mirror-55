try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_lightsail_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_lightsail import *
    except ImportError:
        raise ImportError("Install mypy_boto3[lightsail] to use mypy_boto3.lightsail")
