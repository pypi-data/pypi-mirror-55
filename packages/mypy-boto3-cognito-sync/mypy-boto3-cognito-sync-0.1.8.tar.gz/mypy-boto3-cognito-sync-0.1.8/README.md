# mypy-boto3-cognito-sync submodule

Provides type annotations for `boto3.cognito-sync` service

## Installation

```bash
pip install mypy-boto3[cognito_sync]
```

## Usage

```python
import boto3
from mypy_boto3.cognito_sync import Client, ServiceResource

client: Client = boto3.client("cognito-sync")
resource: ServiceResource = boto3.resource("cognito-sync")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

