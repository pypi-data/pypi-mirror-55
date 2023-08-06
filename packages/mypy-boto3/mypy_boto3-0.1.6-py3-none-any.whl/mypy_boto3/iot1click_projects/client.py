try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_iot1click_projects_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_iot1click_projects.client import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[iot1click-projects] to use mypy_boto3.iot1click_projects"
        )
