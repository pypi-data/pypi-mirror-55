try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_ram_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_ram import *
    except ImportError:
        raise ImportError("Install mypy_boto3[ram] to use mypy_boto3.ram")
