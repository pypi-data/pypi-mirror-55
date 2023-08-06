# mypy-boto3-qldb submodule

Provides type annotations for `boto3.qldb` service

## Installation

```bash
pip install mypy-boto3[qldb]
```

## Usage

```python
import boto3
from mypy_boto3.qldb import Client, ServiceResource

client: Client = boto3.client("qldb")
resource: ServiceResource = boto3.resource("qldb")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

