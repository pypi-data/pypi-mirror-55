# Mypy-boto3 comprehend submodule

Provides type annotations for boto3 comprehend service

## Installation

```bash
pip install mypy-boto3[comprehend]
```

## Usage

```python
import boto3
from mypy_boto3.comprehend import Client, ServiceResource

client: Client = boto3.client("comprehend")
resource: ServiceResource = boto3.resource("comprehend")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

