# mypy-boto3-machinelearning submodule

Provides type annotations for `boto3.machinelearning` service

## Installation

```bash
pip install mypy-boto3[machinelearning]
```

## Usage

```python
import boto3
from mypy_boto3.machinelearning import Client, ServiceResource

client: Client = boto3.client("machinelearning")
resource: ServiceResource = boto3.resource("machinelearning")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

