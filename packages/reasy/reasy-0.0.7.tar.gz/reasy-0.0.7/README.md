# Reasy

A crawler for BT7086 and fast and simple m3u8 downloader.

## Get Start

Download and install [Python3](https://www.python.org/downloads/), [Aria2](https://aria2.github.io/) and [FFmpeg](https://www.ffmpeg.org/), both of them are the key components for Reasy.

Install Reasy. Sometimes you may use `pip3` instead of `pip`, and it also works for `python3` which will be used later on. When you got `reasy version 0.0.4`, it means installation is succeed.

```bash
pip install reasy
reasy -v
```

Set environment variable for Reasy.

- REASY_CONFIG: The path for config of Reasy. Please move `config.yaml.example` to the config folder and rename it to `config.yaml`. To make clear, I presume you move it into `/.reasy/config.yaml`.

```bash
# Linux
export REASY_CONFIG=/.reasy/config.yaml
```

Change config.yaml to meet your requirements. Here we go:

- aria2.config: This is for Aria2, a light-weight downloader. You can use `aria2.conf.example` as template.
- aria2.download_path: The path your videos are saved.
- session.enabled: A mechanism to prevent from download repeated. Unless you know what it is, you should enable it as default.
- session.path: The path for session file. You just need to create a empty file by `touch /.reasy/reasy.session`.

For now, you can run and enjoy it.

```bash
reasy run
# for more usage
reasy run --help
```

## Not Implement Yet

- Get more data if the number of videos not meet the requirements of `maximum_download_num` defined in the `config.yaml` (v0.1.0)
- Multi-threading load m3u8 (v0.1.0)
- Session management by CLI Tool (v0.1.0)
- Web UI to control remotely (v1.0.0)
