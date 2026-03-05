# trye

Ergonomic exception handling for Python.

Inspired by the [ECMAScript Try Operator proposal](https://github.com/arthurfiorette/proposal-try-operator). Instead of `try`/`except` blocks, wrap any callable in `trye()` and get back a typed `Result` — either `Ok(val)` or `Err(err)`.

**Requires Python 3.14+** (uses generic syntax and `type` aliases).

## Install

```bash
uv add trye
```

## Usage

```python
from trye import trye, Ok, Err
```

### isinstance narrowing

```python
result = trye(json.loads, '{"foo": "bar"}')
if isinstance(result, Ok):
    print(result.val)    # dict
else:
    print(result.err)    # Exception
```

### isinstance with else

```python
result = trye(some_function, arg1, arg2)
if isinstance(result, Err):
    log_error(result.err)
    return
# result is narrowed to Ok here
use_value(result.val)
```

### match/case

```python
result = trye(int, user_input)
match result:
    case Ok(val=v):
        print(f"parsed: {v}")
    case Err(err=e):
        print(f"failed: {e}")
```

### Sentinel fields

Both `Ok` and `Err` have sentinel fields so you can always safely check either side:

```python
result = trye(some_function, arg)
if result.err is not None:
    handle_error(result.err)
if result.val is not None:
    use_value(result.val)
```

## API

| Name | Description |
|---|---|
| `trye(f, *args, **kwargs)` | Call `f` with args, return `Ok(result)` or `Err(exception)` |
| `Ok[T]` | Success wrapper. `.val: T`, `.err: None` |
| `Err` | Error wrapper. `.err: Exception`, `.val: None` |
| `Result[T]` | Type alias for `Ok[T] \| Err` |

Arguments are fully typed via `ParamSpec`, so type checkers will catch incorrect arguments to the wrapped function.

## Development

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then:

```bash
uv sync
```

This project uses [poethepoet](https://poethepoet.natn.io/) for tasks:

```bash
uv run poe fmt       # format
uv run poe lint      # lint
uv run poe check     # type check (basedpyright + ty)
uv run poe test      # test

uv run poe all       # all of the above
```

## License

MIT
