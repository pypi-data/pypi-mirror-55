# mypy-boto3-worklink submodule

Provides type annotations for `boto3.worklink` service

## Installation

```bash
pip install mypy-boto3[worklink]
```

## Usage

```python
import boto3
from mypy_boto3.worklink import Client, ServiceResource

client: Client = boto3.client("worklink")
resource: ServiceResource = boto3.resource("worklink")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

