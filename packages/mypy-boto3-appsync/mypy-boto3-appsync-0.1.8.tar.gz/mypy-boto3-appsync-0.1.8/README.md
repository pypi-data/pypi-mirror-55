# mypy-boto3-appsync submodule

Provides type annotations for `boto3.appsync` service

## Installation

```bash
pip install mypy-boto3[appsync]
```

## Usage

```python
import boto3
from mypy_boto3.appsync import Client, ServiceResource

client: Client = boto3.client("appsync")
resource: ServiceResource = boto3.resource("appsync")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

