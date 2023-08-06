# mypy-boto3-guardduty submodule

Provides type annotations for `boto3.guardduty` service

## Installation

```bash
pip install mypy-boto3[guardduty]
```

## Usage

```python
import boto3
from mypy_boto3.guardduty import Client, ServiceResource

client: Client = boto3.client("guardduty")
resource: ServiceResource = boto3.resource("guardduty")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

