# mypy-boto3-sns submodule

Provides type annotations for `boto3.sns` service

## Installation

```bash
pip install mypy-boto3[sns]
```

## Usage

```python
import boto3
from mypy_boto3.sns import Client, ServiceResource

client: Client = boto3.client("sns")
resource: ServiceResource = boto3.resource("sns")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

