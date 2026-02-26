
Tapotalk Plugin

This package provides a standalone, package-local implementation of the Tapotalk
streaming logic and an asyncio-friendly microphone streamer.

Installation
- Create a virtualenv and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the plugin CLI
- From the plugin directory:

```bash
cd tapotalk/tapotalk-plugin
python -m tapotalk_plugin.tapotalk_plugin --host 192.168.1.108 --user admin --cloud-password PASSWORD --super-secret KEY
```