# mypy-boto3-groundstation submodule

Provides type annotations for `boto3.groundstation` service

## Installation

```bash
pip install mypy-boto3[groundstation]
```

## Usage

```python
import boto3
from mypy_boto3.groundstation import Client, ServiceResource

client: Client = boto3.client("groundstation")
resource: ServiceResource = boto3.resource("groundstation")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

