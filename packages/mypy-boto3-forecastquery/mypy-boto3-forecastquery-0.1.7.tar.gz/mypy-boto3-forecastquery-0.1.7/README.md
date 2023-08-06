# mypy-boto3-forecastquery submodule

Provides type annotations for `boto3.forecastquery` service

## Installation

```bash
pip install mypy-boto3[forecastquery]
```

## Usage

```python
import boto3
from mypy_boto3.forecastquery import Client, ServiceResource

client: Client = boto3.client("forecastquery")
resource: ServiceResource = boto3.resource("forecastquery")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

