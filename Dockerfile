FROM python:3.11.2-slim-bullseye

ENV api_url ${api_url}

ENV api_key ${api_key}

ENV discord_token ${discord_token}

ADD bot.py /

ADD adapter_royalroadcom.py /

ADD requirements.txt /

ADD defaults.ini /

RUN pip3 install --upgrade pip

RUN pip install -r requirements.txt



RUN mv -f defaults.ini  /usr/local/lib/python3.11/site-packages/fanficfare/defaults.ini

RUN mv -f adapter_royalroadcom.py /usr/local/lib/python3.11/site-packages/fanficfare/adapters/adapter_royalroadcom.py

CMD python3 bot.py
