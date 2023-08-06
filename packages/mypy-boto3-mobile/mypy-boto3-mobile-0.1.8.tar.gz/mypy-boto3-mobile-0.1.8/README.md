# mypy-boto3-mobile submodule

Provides type annotations for `boto3.mobile` service

## Installation

```bash
pip install mypy-boto3[mobile]
```

## Usage

```python
import boto3
from mypy_boto3.mobile import Client, ServiceResource

client: Client = boto3.client("mobile")
resource: ServiceResource = boto3.resource("mobile")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

