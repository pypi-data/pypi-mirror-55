# Mypy-boto3 textract submodule

Provides type annotations for boto3 textract service

## Installation

```bash
pip install mypy-boto3[textract]
```

## Usage

```python
import boto3
from mypy_boto3.textract import Client, ServiceResource

client: Client = boto3.client("textract")
resource: ServiceResource = boto3.resource("textract")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

