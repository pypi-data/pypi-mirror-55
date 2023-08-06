# mypy-boto3-cloudwatch submodule

Provides type annotations for `boto3.cloudwatch` service

## Installation

```bash
pip install mypy-boto3[cloudwatch]
```

## Usage

```python
import boto3
from mypy_boto3.cloudwatch import Client, ServiceResource

client: Client = boto3.client("cloudwatch")
resource: ServiceResource = boto3.resource("cloudwatch")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

