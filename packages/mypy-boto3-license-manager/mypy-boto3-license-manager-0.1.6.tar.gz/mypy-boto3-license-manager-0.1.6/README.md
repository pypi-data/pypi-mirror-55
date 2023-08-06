# Mypy-boto3 license-manager submodule

Provides type annotations for boto3 license-manager service

## Installation

```bash
pip install mypy-boto3[license-manager]
```

## Usage

```python
import boto3
from mypy_boto3.license_manager import Client, ServiceResource

client: Client = boto3.client("license-manager")
resource: ServiceResource = boto3.resource("license-manager")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

