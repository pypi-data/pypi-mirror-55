# Mypy-boto3 importexport submodule

Provides type annotations for boto3 importexport service

## Installation

```bash
pip install mypy-boto3[importexport]
```

## Usage

```python
import boto3
from mypy_boto3.importexport import Client, ServiceResource

client: Client = boto3.client("importexport")
resource: ServiceResource = boto3.resource("importexport")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

