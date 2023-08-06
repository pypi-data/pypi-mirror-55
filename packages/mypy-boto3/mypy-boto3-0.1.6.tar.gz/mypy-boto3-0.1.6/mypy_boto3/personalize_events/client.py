try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_personalize_events_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_personalize_events.client import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[personalize-events] to use mypy_boto3.personalize_events"
        )
