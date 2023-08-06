try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_events_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_events.client import *
    except ImportError:
        raise ImportError("Install mypy_boto3[events] to use mypy_boto3.events")
