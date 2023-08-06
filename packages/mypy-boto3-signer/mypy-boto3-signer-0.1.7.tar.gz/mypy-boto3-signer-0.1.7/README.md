# mypy-boto3-signer submodule

Provides type annotations for `boto3.signer` service

## Installation

```bash
pip install mypy-boto3[signer]
```

## Usage

```python
import boto3
from mypy_boto3.signer import Client, ServiceResource

client: Client = boto3.client("signer")
resource: ServiceResource = boto3.resource("signer")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

