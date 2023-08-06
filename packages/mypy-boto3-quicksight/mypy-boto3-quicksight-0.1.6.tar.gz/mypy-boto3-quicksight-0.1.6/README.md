# Mypy-boto3 quicksight submodule

Provides type annotations for boto3 quicksight service

## Installation

```bash
pip install mypy-boto3[quicksight]
```

## Usage

```python
import boto3
from mypy_boto3.quicksight import Client, ServiceResource

client: Client = boto3.client("quicksight")
resource: ServiceResource = boto3.resource("quicksight")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

