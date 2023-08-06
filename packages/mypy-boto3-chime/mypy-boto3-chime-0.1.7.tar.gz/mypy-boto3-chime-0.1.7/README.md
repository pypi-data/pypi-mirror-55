# mypy-boto3-chime submodule

Provides type annotations for `boto3.chime` service

## Installation

```bash
pip install mypy-boto3[chime]
```

## Usage

```python
import boto3
from mypy_boto3.chime import Client, ServiceResource

client: Client = boto3.client("chime")
resource: ServiceResource = boto3.resource("chime")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

