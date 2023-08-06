# mypy-boto3-sdb submodule

Provides type annotations for `boto3.sdb` service

## Installation

```bash
pip install mypy-boto3[sdb]
```

## Usage

```python
import boto3
from mypy_boto3.sdb import Client, ServiceResource

client: Client = boto3.client("sdb")
resource: ServiceResource = boto3.resource("sdb")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

