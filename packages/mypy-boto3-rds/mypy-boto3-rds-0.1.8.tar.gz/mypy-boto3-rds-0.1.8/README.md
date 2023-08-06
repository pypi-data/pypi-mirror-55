# mypy-boto3-rds submodule

Provides type annotations for `boto3.rds` service

## Installation

```bash
pip install mypy-boto3[rds]
```

## Usage

```python
import boto3
from mypy_boto3.rds import Client, ServiceResource

client: Client = boto3.client("rds")
resource: ServiceResource = boto3.resource("rds")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

