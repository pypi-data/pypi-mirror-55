# mypy-boto3-forecast submodule

Provides type annotations for `boto3.forecast` service

## Installation

```bash
pip install mypy-boto3[forecast]
```

## Usage

```python
import boto3
from mypy_boto3.forecast import Client, ServiceResource

client: Client = boto3.client("forecast")
resource: ServiceResource = boto3.resource("forecast")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

