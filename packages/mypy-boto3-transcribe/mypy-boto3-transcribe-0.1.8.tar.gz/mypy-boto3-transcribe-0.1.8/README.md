# mypy-boto3-transcribe submodule

Provides type annotations for `boto3.transcribe` service

## Installation

```bash
pip install mypy-boto3[transcribe]
```

## Usage

```python
import boto3
from mypy_boto3.transcribe import Client, ServiceResource

client: Client = boto3.client("transcribe")
resource: ServiceResource = boto3.resource("transcribe")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

