# Mypy-boto3 marketplacecommerceanalytics submodule

Provides type annotations for boto3 marketplacecommerceanalytics service

## Installation

```bash
pip install mypy-boto3[marketplacecommerceanalytics]
```

## Usage

```python
import boto3
from mypy_boto3.marketplacecommerceanalytics import Client, ServiceResource

client: Client = boto3.client("marketplacecommerceanalytics")
resource: ServiceResource = boto3.resource("marketplacecommerceanalytics")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

