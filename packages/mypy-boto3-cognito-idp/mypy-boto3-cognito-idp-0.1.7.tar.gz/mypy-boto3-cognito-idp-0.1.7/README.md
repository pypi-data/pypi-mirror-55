# mypy-boto3-cognito-idp submodule

Provides type annotations for `boto3.cognito-idp` service

## Installation

```bash
pip install mypy-boto3[cognito_idp]
```

## Usage

```python
import boto3
from mypy_boto3.cognito_idp import Client, ServiceResource

client: Client = boto3.client("cognito-idp")
resource: ServiceResource = boto3.resource("cognito-idp")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

