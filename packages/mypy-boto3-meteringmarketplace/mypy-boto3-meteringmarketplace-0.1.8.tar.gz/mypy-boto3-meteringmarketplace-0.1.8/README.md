# mypy-boto3-meteringmarketplace submodule

Provides type annotations for `boto3.meteringmarketplace` service

## Installation

```bash
pip install mypy-boto3[meteringmarketplace]
```

## Usage

```python
import boto3
from mypy_boto3.meteringmarketplace import Client, ServiceResource

client: Client = boto3.client("meteringmarketplace")
resource: ServiceResource = boto3.resource("meteringmarketplace")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

