# mypy-boto3-savingsplans submodule

Provides type annotations for `boto3.savingsplans` service

## Installation

```bash
pip install mypy-boto3[savingsplans]
```

## Usage

```python
import boto3
from mypy_boto3.savingsplans import Client, ServiceResource

client: Client = boto3.client("savingsplans")
resource: ServiceResource = boto3.resource("savingsplans")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

