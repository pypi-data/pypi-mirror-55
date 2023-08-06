# Mypy-boto3 apigatewayv2 submodule

Provides type annotations for boto3 apigatewayv2 service

## Installation

```bash
pip install mypy-boto3[apigatewayv2]
```

## Usage

```python
import boto3
from mypy_boto3.apigatewayv2 import Client, ServiceResource

client: Client = boto3.client("apigatewayv2")
resource: ServiceResource = boto3.resource("apigatewayv2")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

