# mypy-boto3-pinpoint-email submodule

Provides type annotations for `boto3.pinpoint-email` service

## Installation

```bash
pip install mypy-boto3[pinpoint_email]
```

## Usage

```python
import boto3
from mypy_boto3.pinpoint_email import Client, ServiceResource

client: Client = boto3.client("pinpoint-email")
resource: ServiceResource = boto3.resource("pinpoint-email")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

