# Mypy-boto3 alexaforbusiness submodule

Provides type annotations for boto3 alexaforbusiness service

## Installation

```bash
pip install mypy-boto3[alexaforbusiness]
```

## Usage

```python
import boto3
from mypy_boto3.alexaforbusiness import Client, ServiceResource

client: Client = boto3.client("alexaforbusiness")
resource: ServiceResource = boto3.resource("alexaforbusiness")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

