# Mypy-boto3 glacier submodule

Provides type annotations for boto3 glacier service

## Installation

```bash
pip install mypy-boto3[glacier]
```

## Usage

```python
import boto3
from mypy_boto3.glacier import Client, ServiceResource

client: Client = boto3.client("glacier")
resource: ServiceResource = boto3.resource("glacier")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

