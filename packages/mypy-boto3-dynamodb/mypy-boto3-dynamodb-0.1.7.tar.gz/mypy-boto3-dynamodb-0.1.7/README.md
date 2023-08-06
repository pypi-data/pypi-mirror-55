# mypy-boto3-dynamodb submodule

Provides type annotations for `boto3.dynamodb` service

## Installation

```bash
pip install mypy-boto3[dynamodb]
```

## Usage

```python
import boto3
from mypy_boto3.dynamodb import Client, ServiceResource

client: Client = boto3.client("dynamodb")
resource: ServiceResource = boto3.resource("dynamodb")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

