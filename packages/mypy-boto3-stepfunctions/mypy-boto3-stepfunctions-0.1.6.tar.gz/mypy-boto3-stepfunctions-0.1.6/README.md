# Mypy-boto3 stepfunctions submodule

Provides type annotations for boto3 stepfunctions service

## Installation

```bash
pip install mypy-boto3[stepfunctions]
```

## Usage

```python
import boto3
from mypy_boto3.stepfunctions import Client, ServiceResource

client: Client = boto3.client("stepfunctions")
resource: ServiceResource = boto3.resource("stepfunctions")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

