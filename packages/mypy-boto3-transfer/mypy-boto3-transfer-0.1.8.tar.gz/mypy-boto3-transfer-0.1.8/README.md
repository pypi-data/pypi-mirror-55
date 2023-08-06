# mypy-boto3-transfer submodule

Provides type annotations for `boto3.transfer` service

## Installation

```bash
pip install mypy-boto3[transfer]
```

## Usage

```python
import boto3
from mypy_boto3.transfer import Client, ServiceResource

client: Client = boto3.client("transfer")
resource: ServiceResource = boto3.resource("transfer")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

