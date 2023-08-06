# mypy-boto3-batch submodule

Provides type annotations for `boto3.batch` service

## Installation

```bash
pip install mypy-boto3[batch]
```

## Usage

```python
import boto3
from mypy_boto3.batch import Client, ServiceResource

client: Client = boto3.client("batch")
resource: ServiceResource = boto3.resource("batch")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

