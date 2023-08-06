# mypy-boto3-directconnect submodule

Provides type annotations for `boto3.directconnect` service

## Installation

```bash
pip install mypy-boto3[directconnect]
```

## Usage

```python
import boto3
from mypy_boto3.directconnect import Client, ServiceResource

client: Client = boto3.client("directconnect")
resource: ServiceResource = boto3.resource("directconnect")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

