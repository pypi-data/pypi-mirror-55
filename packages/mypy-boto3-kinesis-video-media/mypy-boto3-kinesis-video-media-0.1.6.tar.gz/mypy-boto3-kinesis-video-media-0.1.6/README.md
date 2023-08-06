# Mypy-boto3 kinesis-video-media submodule

Provides type annotations for boto3 kinesis-video-media service

## Installation

```bash
pip install mypy-boto3[kinesis-video-media]
```

## Usage

```python
import boto3
from mypy_boto3.kinesis_video_media import Client, ServiceResource

client: Client = boto3.client("kinesis-video-media")
resource: ServiceResource = boto3.resource("kinesis-video-media")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

