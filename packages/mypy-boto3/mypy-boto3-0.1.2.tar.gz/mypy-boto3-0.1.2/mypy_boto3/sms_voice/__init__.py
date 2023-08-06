try:
    # pylint: disable=wildcard-import, unused-wildcard-import
    from mypy_boto3_sms_voice_with_docs import *
except ImportError:
    try:
        # pylint: disable=wildcard-import, unused-wildcard-import
        from mypy_boto3_sms_voice import *
    except ImportError:
        raise ImportError("Install mypy_boto3[sms-voice] to use mypy_boto3.sms_voice")
