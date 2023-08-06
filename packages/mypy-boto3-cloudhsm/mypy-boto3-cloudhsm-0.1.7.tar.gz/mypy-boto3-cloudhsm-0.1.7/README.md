# mypy-boto3-cloudhsm submodule

Provides type annotations for `boto3.cloudhsm` service

## Installation

```bash
pip install mypy-boto3[cloudhsm]
```

## Usage

```python
import boto3
from mypy_boto3.cloudhsm import Client, ServiceResource

client: Client = boto3.client("cloudhsm")
resource: ServiceResource = boto3.resource("cloudhsm")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

