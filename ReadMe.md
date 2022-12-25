# GPT3-Signalbot

Tired of replying to your Signal messages? Let GPT-3 take care of it.

<div align="center" style="height: 100px>
  <img src="https://github.com/mcschmitz/gpt3-signalbot/blob/doc-and-test/gif/ezgif-5-e93d89a10b.gif">
</div>

This repository is based on [René Filip's signalbot](https://github.com/filipre/signalbot), and [bbernhard's Signal CLI REST Api](https://github.com/bbernhard/signal-cli-rest-api)

## ⚙️ Setup
To run, please make sure that you have Python 3.9, and docker installed. To install the dependencies run

```bash
pip install poetry
poetry install
```

## 🏃 Get it running
1. Create a directory for the configuration. This allows you to update [signal-cli-rest-api](https://github.com/bbernhard/signal-cli-rest-api) by just deleting and recreating the container without the need to re-register your signal number
```
export SIGNAL_CLI=$HOME/.local/share/signal-cli
mkdir $SIGNAL_CLI
```
2. Now ramp up the the REST API and register our Signal Number.
```bash
docker run --restart=always -p 8080:8080 \
      -v $SIGNAL_CLI:/home/.local/share/signal-cli \
      -e 'MODE=native' bbernhard/signal-cli-rest-api
```
Open http://localhost:8080/v1/qrcodelink?device_name=signal-api in your browser, open Signal on your mobile phone, go to Settings > Linked devices and scan the QR code using the + button.

3. Restart the server in `json-rpc` mode.
```bash
docker run --restart=always -p 8080:8080 \
    -v $SIGNAL_CLI:/home/.local/share/signal-cli \
    -e 'MODE=json-rpc' bbernhard/signal-cli-rest-api
```
As soon as the logs show `time="2022-12-23T17:30:03Z" level=info msg="Started Signal Messenger REST API"` the API is started successfully.

4. Now that the API has started, we can start the bot by running `poetry run python bot.py --service 127.0.0.1:8080 --phone_number <Your-Phone-Number>`