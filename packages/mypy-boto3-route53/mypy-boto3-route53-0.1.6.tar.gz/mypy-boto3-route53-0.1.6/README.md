# Mypy-boto3 route53 submodule

Provides type annotations for boto3 route53 service

## Installation

```bash
pip install mypy-boto3[route53]
```

## Usage

```python
import boto3
from mypy_boto3.route53 import Client, ServiceResource

client: Client = boto3.client("route53")
resource: ServiceResource = boto3.resource("route53")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

