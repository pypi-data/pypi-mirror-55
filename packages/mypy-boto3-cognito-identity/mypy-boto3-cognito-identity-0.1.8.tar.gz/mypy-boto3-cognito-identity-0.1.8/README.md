# mypy-boto3-cognito-identity submodule

Provides type annotations for `boto3.cognito-identity` service

## Installation

```bash
pip install mypy-boto3[cognito_identity]
```

## Usage

```python
import boto3
from mypy_boto3.cognito_identity import Client, ServiceResource

client: Client = boto3.client("cognito-identity")
resource: ServiceResource = boto3.resource("cognito-identity")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

