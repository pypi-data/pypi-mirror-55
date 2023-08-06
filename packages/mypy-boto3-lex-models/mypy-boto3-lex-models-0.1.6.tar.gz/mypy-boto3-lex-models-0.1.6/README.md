# Mypy-boto3 lex-models submodule

Provides type annotations for boto3 lex-models service

## Installation

```bash
pip install mypy-boto3[lex-models]
```

## Usage

```python
import boto3
from mypy_boto3.lex_models import Client, ServiceResource

client: Client = boto3.client("lex-models")
resource: ServiceResource = boto3.resource("lex-models")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

