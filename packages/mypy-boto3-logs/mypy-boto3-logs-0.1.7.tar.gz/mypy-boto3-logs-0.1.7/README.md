# mypy-boto3-logs submodule

Provides type annotations for `boto3.logs` service

## Installation

```bash
pip install mypy-boto3[logs]
```

## Usage

```python
import boto3
from mypy_boto3.logs import Client, ServiceResource

client: Client = boto3.client("logs")
resource: ServiceResource = boto3.resource("logs")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

