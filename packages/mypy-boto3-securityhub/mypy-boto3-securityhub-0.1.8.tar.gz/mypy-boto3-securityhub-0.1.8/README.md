# mypy-boto3-securityhub submodule

Provides type annotations for `boto3.securityhub` service

## Installation

```bash
pip install mypy-boto3[securityhub]
```

## Usage

```python
import boto3
from mypy_boto3.securityhub import Client, ServiceResource

client: Client = boto3.client("securityhub")
resource: ServiceResource = boto3.resource("securityhub")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

