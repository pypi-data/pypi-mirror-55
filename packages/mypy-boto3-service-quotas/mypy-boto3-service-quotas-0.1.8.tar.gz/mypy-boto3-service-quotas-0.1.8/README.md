# mypy-boto3-service-quotas submodule

Provides type annotations for `boto3.service-quotas` service

## Installation

```bash
pip install mypy-boto3[service_quotas]
```

## Usage

```python
import boto3
from mypy_boto3.service_quotas import Client, ServiceResource

client: Client = boto3.client("service-quotas")
resource: ServiceResource = boto3.resource("service-quotas")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

