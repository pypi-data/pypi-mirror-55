# Mypy-boto3 kinesis-video-archived-media submodule

Provides type annotations for boto3 kinesis-video-archived-media service

## Installation

```bash
pip install mypy-boto3[kinesis-video-archived-media]
```

## Usage

```python
import boto3
from mypy_boto3.kinesis_video_archived_media import Client, ServiceResource

client: Client = boto3.client("kinesis-video-archived-media")
resource: ServiceResource = boto3.resource("kinesis-video-archived-media")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

