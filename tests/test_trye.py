from trye import Err, Ok, trye


def somefunc(foo: str) -> int:
    print(foo)
    return 2


def failfunc(foo: str) -> int:
    raise ValueError(f"bad: {foo}")


def takes_int(v: int) -> None:
    assert isinstance(v, int)


def test_isinstance_ok() -> None:
    result = trye(somefunc, "hiya")
    if isinstance(result, Ok):
        takes_int(result.val)
    else:
        raise AssertionError("Expected Ok")


def test_isinstance_err() -> None:
    result = trye(failfunc, "hiya")
    if isinstance(result, Err):
        assert isinstance(result.err, ValueError)
    else:
        raise AssertionError("Expected Err")


def test_isinstance_else() -> None:
    result = trye(somefunc, "hiya")
    if isinstance(result, Err):
        raise AssertionError("Expected Ok")
    else:
        takes_int(result.val)


def test_match_ok() -> None:
    result = trye(somefunc, "hiya")
    match result:
        case Ok(val=v):
            takes_int(v)
        case Err(err=e):
            raise AssertionError(f"Expected Ok, got Err: {e}")


def test_match_err() -> None:
    result = trye(failfunc, "hiya")
    match result:
        case Ok(val=v):
            raise AssertionError(f"Expected Err, got Ok: {v}")
        case Err(err=e):
            assert isinstance(e, ValueError)


def test_ok_sentinel_fields() -> None:
    result = trye(somefunc, "hiya")
    assert isinstance(result, Ok)
    assert result.err is None
    assert result.val == 2


def test_err_sentinel_fields() -> None:
    result = trye(failfunc, "hiya")
    assert isinstance(result, Err)
    assert result.val is None
    assert isinstance(result.err, ValueError)


def test_lambda() -> None:
    r = trye(lambda: failfunc("hiya"))
    match r:
        case Ok(val=v):
            raise AssertionError(f"Expected Err, got Ok: {v}")
        case Err(err=e):
            assert isinstance(e, ValueError)
