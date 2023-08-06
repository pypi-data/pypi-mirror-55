# mypy-boto3-kinesisvideo submodule

Provides type annotations for `boto3.kinesisvideo` service

## Installation

```bash
pip install mypy-boto3[kinesisvideo]
```

## Usage

```python
import boto3
from mypy_boto3.kinesisvideo import Client, ServiceResource

client: Client = boto3.client("kinesisvideo")
resource: ServiceResource = boto3.resource("kinesisvideo")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

