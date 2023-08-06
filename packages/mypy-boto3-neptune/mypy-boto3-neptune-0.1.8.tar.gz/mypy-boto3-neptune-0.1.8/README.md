# mypy-boto3-neptune submodule

Provides type annotations for `boto3.neptune` service

## Installation

```bash
pip install mypy-boto3[neptune]
```

## Usage

```python
import boto3
from mypy_boto3.neptune import Client, ServiceResource

client: Client = boto3.client("neptune")
resource: ServiceResource = boto3.resource("neptune")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

