# mypy-boto3-sqs submodule

Provides type annotations for `boto3.sqs` service

## Installation

```bash
pip install mypy-boto3[sqs]
```

## Usage

```python
import boto3
from mypy_boto3.sqs import Client, ServiceResource

client: Client = boto3.client("sqs")
resource: ServiceResource = boto3.resource("sqs")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

