# mypy-boto3-polly submodule

Provides type annotations for `boto3.polly` service

## Installation

```bash
pip install mypy-boto3[polly]
```

## Usage

```python
import boto3
from mypy_boto3.polly import Client, ServiceResource

client: Client = boto3.client("polly")
resource: ServiceResource = boto3.resource("polly")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

