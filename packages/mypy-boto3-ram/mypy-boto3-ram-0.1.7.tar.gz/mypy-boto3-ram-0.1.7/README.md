# mypy-boto3-ram submodule

Provides type annotations for `boto3.ram` service

## Installation

```bash
pip install mypy-boto3[ram]
```

## Usage

```python
import boto3
from mypy_boto3.ram import Client, ServiceResource

client: Client = boto3.client("ram")
resource: ServiceResource = boto3.resource("ram")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

