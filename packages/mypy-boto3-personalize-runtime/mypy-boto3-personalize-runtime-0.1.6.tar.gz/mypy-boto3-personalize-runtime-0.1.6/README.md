# Mypy-boto3 personalize-runtime submodule

Provides type annotations for boto3 personalize-runtime service

## Installation

```bash
pip install mypy-boto3[personalize-runtime]
```

## Usage

```python
import boto3
from mypy_boto3.personalize_runtime import Client, ServiceResource

client: Client = boto3.client("personalize-runtime")
resource: ServiceResource = boto3.resource("personalize-runtime")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

