# mypy-boto3-acm submodule

Provides type annotations for `boto3.acm` service

## Installation

```bash
pip install mypy-boto3[acm]
```

## Usage

```python
import boto3
from mypy_boto3.acm import Client, ServiceResource

client: Client = boto3.client("acm")
resource: ServiceResource = boto3.resource("acm")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

