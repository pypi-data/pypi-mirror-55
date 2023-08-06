# mypy-boto3-lex-runtime submodule

Provides type annotations for `boto3.lex-runtime` service

## Installation

```bash
pip install mypy-boto3[lex_runtime]
```

## Usage

```python
import boto3
from mypy_boto3.lex_runtime import Client, ServiceResource

client: Client = boto3.client("lex-runtime")
resource: ServiceResource = boto3.resource("lex-runtime")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

