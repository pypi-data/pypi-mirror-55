# mypy-boto3-dlm submodule

Provides type annotations for `boto3.dlm` service

## Installation

```bash
pip install mypy-boto3[dlm]
```

## Usage

```python
import boto3
from mypy_boto3.dlm import Client, ServiceResource

client: Client = boto3.client("dlm")
resource: ServiceResource = boto3.resource("dlm")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

