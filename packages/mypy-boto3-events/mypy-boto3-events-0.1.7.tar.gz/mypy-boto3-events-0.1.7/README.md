# mypy-boto3-events submodule

Provides type annotations for `boto3.events` service

## Installation

```bash
pip install mypy-boto3[events]
```

## Usage

```python
import boto3
from mypy_boto3.events import Client, ServiceResource

client: Client = boto3.client("events")
resource: ServiceResource = boto3.resource("events")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

