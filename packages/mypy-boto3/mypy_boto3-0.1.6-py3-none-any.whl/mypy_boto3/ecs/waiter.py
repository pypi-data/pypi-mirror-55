try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_ecs_with_docs.waiter import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_ecs.waiter import *
    except ImportError:
        raise ImportError("Install mypy_boto3[ecs] to use mypy_boto3.ecs")
