# mypy-boto3-secretsmanager submodule

Provides type annotations for `boto3.secretsmanager` service

## Installation

```bash
pip install mypy-boto3[secretsmanager]
```

## Usage

```python
import boto3
from mypy_boto3.secretsmanager import Client, ServiceResource

client: Client = boto3.client("secretsmanager")
resource: ServiceResource = boto3.resource("secretsmanager")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

