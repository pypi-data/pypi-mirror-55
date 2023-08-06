try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_personalize_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_personalize import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[personalize] to use mypy_boto3.personalize"
        )
