from core.hunt import hunter


def test_hunter_retry_or_notify():
    attempt_num = 0
    retry_count = 2

    @hunter(retries=retry_count)
    def total_attempts():
        nonlocal attempt_num
        attempt_num += 1
        if attempt_num <= retry_count:
            raise Exception('this exception should be caught, and the wrapped_test func should be retried.')
        return attempt_num

    assert total_attempts() == retry_count + 1
