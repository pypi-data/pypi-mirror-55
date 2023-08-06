# mypy-boto3-ecr submodule

Provides type annotations for `boto3.ecr` service

## Installation

```bash
pip install mypy-boto3[ecr]
```

## Usage

```python
import boto3
from mypy_boto3.ecr import Client, ServiceResource

client: Client = boto3.client("ecr")
resource: ServiceResource = boto3.resource("ecr")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

