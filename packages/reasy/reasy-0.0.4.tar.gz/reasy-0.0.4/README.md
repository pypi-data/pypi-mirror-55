# BT7086 Downloader

A crawler for BT7086 and fast and simple m3u8 downloader.

## Requirements

- Aria2 for multi-threading download
- FFmpeg for merging video segments

## Environment Variables

- BT7086_CONFIG

## Not Implement Yet

- Get more data if the number of videos not meet the requirements of `maximum_download_num` defined in the `config.yaml` (v0.0.3)
- Multi-threading load m3u8 (v0.0.3)
- Web UI to control remotely (v0.0.4)
- ~~Command line support (v0.0.2)~~
- ~~Session mechanism to avoid downloading repeatedly (v0.0.2)~~
- ~~Verify status of FFmpeg installation before merging (v0.0.2)~~
- ~~Get stats of current task (v0.0.2)~~
