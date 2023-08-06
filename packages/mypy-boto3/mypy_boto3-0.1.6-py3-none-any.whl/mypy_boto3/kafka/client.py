try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_kafka_with_docs.client import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_kafka.client import *
    except ImportError:
        raise ImportError("Install mypy_boto3[kafka] to use mypy_boto3.kafka")
