# Mypy-boto3 globalaccelerator submodule

Provides type annotations for boto3 globalaccelerator service

## Installation

```bash
pip install mypy-boto3[globalaccelerator]
```

## Usage

```python
import boto3
from mypy_boto3.globalaccelerator import Client, ServiceResource

client: Client = boto3.client("globalaccelerator")
resource: ServiceResource = boto3.resource("globalaccelerator")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

