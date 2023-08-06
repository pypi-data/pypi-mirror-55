# Mypy-boto3 amplify submodule

Provides type annotations for boto3 amplify service

## Installation

```bash
pip install mypy-boto3[amplify]
```

## Usage

```python
import boto3
from mypy_boto3.amplify import Client, ServiceResource

client: Client = boto3.client("amplify")
resource: ServiceResource = boto3.resource("amplify")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

