FROM python:3.10

WORKDIR /btc_wallets_api
COPY requirements.txt /btc_wallets_api
RUN pip3 install -r /btc_wallets_api/requirements.txt
COPY . /btc_wallets_api
