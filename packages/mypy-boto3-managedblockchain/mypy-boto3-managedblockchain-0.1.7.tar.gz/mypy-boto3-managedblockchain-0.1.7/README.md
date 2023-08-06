# mypy-boto3-managedblockchain submodule

Provides type annotations for `boto3.managedblockchain` service

## Installation

```bash
pip install mypy-boto3[managedblockchain]
```

## Usage

```python
import boto3
from mypy_boto3.managedblockchain import Client, ServiceResource

client: Client = boto3.client("managedblockchain")
resource: ServiceResource = boto3.resource("managedblockchain")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

