# mypy-boto3-pricing submodule

Provides type annotations for `boto3.pricing` service

## Installation

```bash
pip install mypy-boto3[pricing]
```

## Usage

```python
import boto3
from mypy_boto3.pricing import Client, ServiceResource

client: Client = boto3.client("pricing")
resource: ServiceResource = boto3.resource("pricing")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

