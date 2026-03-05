import pytest

from trye import Err, Ok, is_err, is_ok, trye


def somefunc(foo: str) -> int:
    print(foo)
    return 2


def failfunc(foo: str) -> int:
    raise ValueError(f"bad: {foo}")


def takes_int(v: int) -> None:
    assert isinstance(v, int)


# --- is_ok / is_err ---


def test_is_ok() -> None:
    result = trye(somefunc, "hiya")
    assert is_ok(result)
    assert not is_err(result)


def test_is_err() -> None:
    result = trye(failfunc, "hiya")
    assert is_err(result)
    assert not is_ok(result)


def test_is_ok_narrowing() -> None:
    result = trye(somefunc, "hiya")
    if is_ok(result):
        takes_int(result.val)
    else:
        raise AssertionError("Expected Ok")


def test_is_err_narrowing() -> None:
    result = trye(failfunc, "hiya")
    if is_err(result):
        assert isinstance(result.err, ValueError)
    else:
        raise AssertionError("Expected Err")


def test_is_ok_else() -> None:
    result = trye(failfunc, "hiya")
    if is_ok(result):
        raise AssertionError("Expected Err")
    else:
        assert isinstance(result.err, ValueError)


# --- match/case ---


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


# --- unwrap ---


def test_unwrap_ok() -> None:
    result = trye(somefunc, "hiya")
    assert result.unwrap() == 2


def test_unwrap_err() -> None:
    result = trye(failfunc, "hiya")
    with pytest.raises(ValueError, match="bad: hiya"):
        result.unwrap()


# --- unwrap_or ---


def test_unwrap_or_ok() -> None:
    result = trye(somefunc, "hiya")
    assert result.unwrap_or(99) == 2


def test_unwrap_or_err() -> None:
    result = trye(failfunc, "hiya")
    assert result.unwrap_or(99) == 99


def test_unwrap_or_ok_direct() -> None:
    assert Ok(42).unwrap_or(0) == 42


def test_unwrap_or_err_direct() -> None:
    err: Err[int] = Err(ValueError("oops"))
    assert err.unwrap_or(0) == 0


# --- sentinel fields ---


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


# --- lambda ---


def test_lambda() -> None:
    r = trye(lambda: failfunc("hiya"))
    match r:
        case Ok(val=v):
            raise AssertionError(f"Expected Err, got Ok: {v}")
        case Err(err=e):
            assert isinstance(e, ValueError)
