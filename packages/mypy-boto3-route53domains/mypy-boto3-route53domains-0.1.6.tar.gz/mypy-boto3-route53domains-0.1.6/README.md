# Mypy-boto3 route53domains submodule

Provides type annotations for boto3 route53domains service

## Installation

```bash
pip install mypy-boto3[route53domains]
```

## Usage

```python
import boto3
from mypy_boto3.route53domains import Client, ServiceResource

client: Client = boto3.client("route53domains")
resource: ServiceResource = boto3.resource("route53domains")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

