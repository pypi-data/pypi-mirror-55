# Mypy-boto3 apigatewaymanagementapi submodule

Provides type annotations for boto3 apigatewaymanagementapi service

## Installation

```bash
pip install mypy-boto3[apigatewaymanagementapi]
```

## Usage

```python
import boto3
from mypy_boto3.apigatewaymanagementapi import Client, ServiceResource

client: Client = boto3.client("apigatewaymanagementapi")
resource: ServiceResource = boto3.resource("apigatewaymanagementapi")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

