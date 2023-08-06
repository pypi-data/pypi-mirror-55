# Mypy-boto3 marketplace-entitlement submodule

Provides type annotations for boto3 marketplace-entitlement service

## Installation

```bash
pip install mypy-boto3[marketplace-entitlement]
```

## Usage

```python
import boto3
from mypy_boto3.marketplace_entitlement import Client, ServiceResource

client: Client = boto3.client("marketplace-entitlement")
resource: ServiceResource = boto3.resource("marketplace-entitlement")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

