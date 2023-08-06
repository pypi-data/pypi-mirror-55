# mypy-boto3-robomaker submodule

Provides type annotations for `boto3.robomaker` service

## Installation

```bash
pip install mypy-boto3[robomaker]
```

## Usage

```python
import boto3
from mypy_boto3.robomaker import Client, ServiceResource

client: Client = boto3.client("robomaker")
resource: ServiceResource = boto3.resource("robomaker")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

