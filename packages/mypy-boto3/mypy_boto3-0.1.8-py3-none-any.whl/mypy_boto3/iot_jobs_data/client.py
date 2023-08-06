try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_iot_jobs_data_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_iot_jobs_data.client import *  # type: ignore
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[iot-jobs-data] to use mypy_boto3.iot_jobs_data"
        )
