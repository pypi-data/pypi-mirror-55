# mypy-boto3-apigateway submodule

Provides type annotations for `boto3.apigateway` service

## Installation

```bash
pip install mypy-boto3[apigateway]
```

## Usage

```python
import boto3
from mypy_boto3.apigateway import Client, ServiceResource

client: Client = boto3.client("apigateway")
resource: ServiceResource = boto3.resource("apigateway")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

