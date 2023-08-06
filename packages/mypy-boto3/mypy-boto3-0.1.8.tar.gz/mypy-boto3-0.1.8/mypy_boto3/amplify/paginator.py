try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_amplify_with_docs.paginator import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_amplify.paginator import *  # type: ignore
    except ImportError:
        raise ImportError("Install mypy_boto3[amplify] to use mypy_boto3.amplify")
