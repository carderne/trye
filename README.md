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
from trye import trye, is_ok, is_err, Ok, Err
```

### Wrapping a function call

Pass the function and its arguments directly:

```python
result = trye(json.loads, '{"foo": "bar"}')
```

Or use a lambda for more complex expressions:

```python
result = trye(lambda: db.query("SELECT * FROM users"))
```

### Checking and narrowing

`is_ok()` and `is_err()` check the result and narrow the type for your type checker:

```python
result = trye(json.loads, '{"foo": "bar"}')
if is_ok(result):
    print(result.val)    # dict
else:
    print(result.err)    # Exception
```

```python
result = trye(some_function, arg1, arg2)
if is_err(result):
    log_error(result.err)
    return
# result is narrowed to Ok here
use_value(result.val)
```

### unwrap

If you just want the value or to re-raise the exception:

```python
value = trye(json.loads, data).unwrap()
```

`unwrap()` returns the value from `Ok`, or raises the exception from `Err`.

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

### Creating results manually

You can create `Ok` and `Err` objects directly:

```python
from trye import Ok, Err

success = Ok(42)
failure = Err(ValueError("something went wrong"))
```

This is useful for bridging non-trye code, writing tests, or returning results from your own functions:

```python
def parse_config(path: str) -> Result[Config]:
    if not path.endswith(".toml"):
        return Err(ValueError(f"unsupported format: {path}"))
    return Ok(load_toml(path))
```

## API

| Name | Description |
|---|---|
| `trye(f, *args, **kwargs)` | Call `f` with args, return `Ok(result)` or `Err(exception)` |
| `is_ok(result)` | `TypeIs` narrowing to `Ok[T]` |
| `is_err(result)` | `TypeIs` narrowing to `Err` |
| `Ok[T]` | Success wrapper. `.val: T`, `.err: None`, `.unwrap() -> T` |
| `Err` | Error wrapper. `.err: Exception`, `.val: None`, `.unwrap() -> Never` |
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
