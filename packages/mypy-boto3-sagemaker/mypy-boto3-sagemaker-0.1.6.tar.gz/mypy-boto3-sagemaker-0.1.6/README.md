# Mypy-boto3 sagemaker submodule

Provides type annotations for boto3 sagemaker service

## Installation

```bash
pip install mypy-boto3[sagemaker]
```

## Usage

```python
import boto3
from mypy_boto3.sagemaker import Client, ServiceResource

client: Client = boto3.client("sagemaker")
resource: ServiceResource = boto3.resource("sagemaker")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

