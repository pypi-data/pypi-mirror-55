# Mypy-boto3 codestar submodule

Provides type annotations for boto3 codestar service

## Installation

```bash
pip install mypy-boto3[codestar]
```

## Usage

```python
import boto3
from mypy_boto3.codestar import Client, ServiceResource

client: Client = boto3.client("codestar")
resource: ServiceResource = boto3.resource("codestar")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

