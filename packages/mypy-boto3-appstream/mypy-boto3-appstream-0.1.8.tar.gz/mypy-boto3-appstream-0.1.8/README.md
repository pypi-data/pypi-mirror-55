# mypy-boto3-appstream submodule

Provides type annotations for `boto3.appstream` service

## Installation

```bash
pip install mypy-boto3[appstream]
```

## Usage

```python
import boto3
from mypy_boto3.appstream import Client, ServiceResource

client: Client = boto3.client("appstream")
resource: ServiceResource = boto3.resource("appstream")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

