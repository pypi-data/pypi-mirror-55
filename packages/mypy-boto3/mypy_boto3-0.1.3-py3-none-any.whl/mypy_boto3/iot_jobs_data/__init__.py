try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_iot_jobs_data_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_iot_jobs_data import *
    except ImportError:
        raise ImportError(
            "Install mypy_boto3[iot-jobs-data] to use mypy_boto3.iot_jobs_data"
        )
