# Mypy-boto3 personalize submodule

Provides type annotations for boto3 personalize service

## Installation

```bash
pip install mypy-boto3[personalize]
```

## Usage

```python
import boto3
from mypy_boto3.personalize import Client, ServiceResource

client: Client = boto3.client("personalize")
resource: ServiceResource = boto3.resource("personalize")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

