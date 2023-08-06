# mypy-boto3-pi submodule

Provides type annotations for `boto3.pi` service

## Installation

```bash
pip install mypy-boto3[pi]
```

## Usage

```python
import boto3
from mypy_boto3.pi import Client, ServiceResource

client: Client = boto3.client("pi")
resource: ServiceResource = boto3.resource("pi")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

