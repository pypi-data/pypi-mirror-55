# mypy-boto3-athena submodule

Provides type annotations for `boto3.athena` service

## Installation

```bash
pip install mypy-boto3[athena]
```

## Usage

```python
import boto3
from mypy_boto3.athena import Client, ServiceResource

client: Client = boto3.client("athena")
resource: ServiceResource = boto3.resource("athena")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

