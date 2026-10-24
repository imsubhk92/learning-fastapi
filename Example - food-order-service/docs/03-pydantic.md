# 3. Pydantic: more than checking types

## Validation at a boundary

Plain Python annotations help editors and type checkers; Python does not
automatically reject a string passed to a function annotated `count: int`.
Pydantic turns a declared model into runtime parsing, validation and
serialization behavior. FastAPI connects that behavior to HTTP.
[Pydantic models](https://docs.pydantic.dev/latest/concepts/models/).

Our [models](../app/models.py) give different jobs to different contracts:

| Model | Accepted or returned data | Reason |
| --- | --- | --- |
| `OrderCreate` | `item`, `count` only | Clients cannot assign an ID or initial status |
| `OrderStatusUpdate` | Required enum `status` only | Explicit PATCH scope |
| `Order` | `id`, `item`, `count`, `status` | Returned snapshot, immutable fields |
| `OrderPage` | Orders plus pagination metadata | Stable collection envelope |
| `OrderSnapshot` | Event name plus an `Order` | A defined WebSocket payload |

`extra="forbid"` rejects unknown input keys. Item names are trimmed and must
contain 1–120 characters. Counts must be integer JSON numbers from 1 to 100;
booleans, numeric strings and fractional numbers are rejected. The enum limits
status spelling, but it does not enforce whether a delivered order may return
to pending. That workflow rule belongs in the domain layer.

## Coercion versus strict mode

Pydantic normally parses compatible inputs. Strict fields restrict that
conversion. This app chooses strict `count` in JSON while allowing normal
parsing of integer query/path values. Do not apply strict integer validation
to every text query parameter without checking the HTTP parsing behavior.
[Strict mode](https://docs.pydantic.dev/latest/concepts/strict_mode/).

**Standalone REPL example** from the project directory:

```python
from pydantic import ValidationError
from app.models import OrderCreate

order = OrderCreate.model_validate({"item": "  Dal  ", "count": 2})
print(order.item)  # Dal
print(order.model_dump())  # Python dict
print(order.model_dump_json())  # JSON string
print(OrderCreate.model_json_schema())  # Schema metadata

try:
    OrderCreate.model_validate({"item": "Dal", "count": "2"})
except ValidationError as error:
    print(error.errors()[0]["loc"])  # ('count',)
```

The v2 names to remember are `model_validate`, `model_dump`,
`model_dump_json`, and `model_json_schema`. Older tutorials may use v1 names
such as `parse_obj` and `dict`. Use the
[migration guide](https://docs.pydantic.dev/latest/migration/).

## Common advanced tools

| Tool | Use case | Caution |
| --- | --- | --- |
| Nested models | An order with multiple validated line items | Bound list size and nested payload size |
| `field_validator` | A field rule beyond built-in constraints | Raise `ValueError`; keep remote I/O out of validation |
| `model_validator` | A relationship between fields, such as start/end dates | Separate structural rules from database/business decisions |
| Aliases | Map an external JSON name to an internal name | Decide input/output alias policies explicitly |
| `TypeAdapter` | Validate values such as `list[Order]` without a wrapper model | Still requires a clear boundary and error handling |
| Discriminated unions | Several payload kinds identified by a field | Prefer clear tags over ambiguous alternatives |
| Serialization options | Produce JSON-compatible values, include/exclude fields | Serialization is not access control |
| Settings management | Typed environment configuration as settings grow | Separate package; not needed for this app's one flag |

Read [validators](https://docs.pydantic.dev/latest/concepts/validators/),
[serialization](https://docs.pydantic.dev/latest/concepts/serialization/), and
[type adapters](https://docs.pydantic.dev/latest/concepts/type_adapter/).

`Order` is frozen, so assignment to its fields is rejected. The repository
replaces a snapshot on status changes. `model_copy(update=...)` does **not**
validate arbitrary updates: we only use it with an enum already validated by
the request model. Revalidate untrusted merged data with `model_validate`.
Frozen models do not automatically freeze a mutable list nested inside them.

Input validation and output validation have different implications: an invalid
request is a client error, while invalid server output is an application bug.
Response schemas also help prevent accidentally exposing internal fields, but
authorization still has to decide which records a caller can access.
[Response model behavior](https://fastapi.tiangolo.com/tutorial/response-model/).

Checkpoint: explain why `count=true` is rejected, why a valid enum value can
still violate business rules, and why a model matching an expected shape does
not prove AI output is factually correct.
