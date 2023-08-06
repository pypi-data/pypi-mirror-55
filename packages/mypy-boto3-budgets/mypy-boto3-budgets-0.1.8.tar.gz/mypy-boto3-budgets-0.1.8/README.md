# mypy-boto3-budgets submodule

Provides type annotations for `boto3.budgets` service

## Installation

```bash
pip install mypy-boto3[budgets]
```

## Usage

```python
import boto3
from mypy_boto3.budgets import Client, ServiceResource

client: Client = boto3.client("budgets")
resource: ServiceResource = boto3.resource("budgets")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

