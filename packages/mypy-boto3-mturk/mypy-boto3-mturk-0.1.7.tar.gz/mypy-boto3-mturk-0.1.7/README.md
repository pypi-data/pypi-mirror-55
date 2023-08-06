# mypy-boto3-mturk submodule

Provides type annotations for `boto3.mturk` service

## Installation

```bash
pip install mypy-boto3[mturk]
```

## Usage

```python
import boto3
from mypy_boto3.mturk import Client, ServiceResource

client: Client = boto3.client("mturk")
resource: ServiceResource = boto3.resource("mturk")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

