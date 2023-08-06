# mypy-boto3-medialive submodule

Provides type annotations for `boto3.medialive` service

## Installation

```bash
pip install mypy-boto3[medialive]
```

## Usage

```python
import boto3
from mypy_boto3.medialive import Client, ServiceResource

client: Client = boto3.client("medialive")
resource: ServiceResource = boto3.resource("medialive")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

