#!/bin/sh

# FIXME: dialogflow api v1
export DIALOGFLOW_CLIENT_ACCESS_TOKEN="기입"
export DIALOGFLOW_DEVELOPER_ACCESS_TOKEN="기입"
export DIALOGFLOW_WEB_DEMO_URL="https://console.dialogflow.com/api-client/demo/embedded/9e379743-6915-4a6b-8324-6f28bc9644f0"
export JUPYTER_NOTEBOOK_TOKEN="askbot"  # Jupyter Login 암호

# etc
export LC_ALL="ko_KR.UTF-8"
alias python="python3"
alias pip="pip3"

echo "loaded."

