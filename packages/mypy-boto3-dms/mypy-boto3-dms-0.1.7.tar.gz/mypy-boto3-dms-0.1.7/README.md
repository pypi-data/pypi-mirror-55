# mypy-boto3-dms submodule

Provides type annotations for `boto3.dms` service

## Installation

```bash
pip install mypy-boto3[dms]
```

## Usage

```python
import boto3
from mypy_boto3.dms import Client, ServiceResource

client: Client = boto3.client("dms")
resource: ServiceResource = boto3.resource("dms")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

