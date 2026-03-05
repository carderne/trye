import asyncio

import pytest

from trye import atrye, is_err, is_ok


async def async_somefunc(foo: str) -> int:
    await asyncio.sleep(0)
    return len(foo)


async def async_failfunc(foo: str) -> int:
    await asyncio.sleep(0)
    raise ValueError(f"bad: {foo}")


@pytest.mark.asyncio
async def test_atrye_ok() -> None:
    result = await atrye(async_somefunc, "hello")
    assert is_ok(result)
    assert result.val == 5


@pytest.mark.asyncio
async def test_atrye_err() -> None:
    result = await atrye(async_failfunc, "hello")
    assert is_err(result)
    assert isinstance(result.err, ValueError)


@pytest.mark.asyncio
async def test_atrye_unwrap_ok() -> None:
    value = (await atrye(async_somefunc, "hi")).unwrap()
    assert value == 2


@pytest.mark.asyncio
async def test_atrye_unwrap_err() -> None:
    with pytest.raises(ValueError, match="bad: hi"):
        (await atrye(async_failfunc, "hi")).unwrap()


@pytest.mark.asyncio
async def test_atrye_unwrap_or() -> None:
    value = (await atrye(async_failfunc, "hi")).unwrap_or(-1)
    assert value == -1
