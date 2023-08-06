# mypy-boto3-snowball submodule

Provides type annotations for `boto3.snowball` service

## Installation

```bash
pip install mypy-boto3[snowball]
```

## Usage

```python
import boto3
from mypy_boto3.snowball import Client, ServiceResource

client: Client = boto3.client("snowball")
resource: ServiceResource = boto3.resource("snowball")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

