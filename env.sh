#!/bin/sh

# FIXME: dialogflow api v1
export DIALOGFLOW_CLIENT_ACCESS_TOKEN="2cc2dcfc7c7540a591cfcf8629e0696d"
export DIALOGFLOW_DEVELOPER_ACCESS_TOKEN="72e767493b8648e9ad94cfa7fe292a23"
export DIALOGFLOW_WEB_DEMO_URL="https://console.dialogflow.com/api-client/demo/embedded/9e379743-6915-4a6b-8324-6f28bc9644f0"
export JUPYTER_NOTEBOOK_TOKEN="askbot"  # Jupyter Login 암호

# etc
export LC_ALL="ko_KR.UTF-8"
alias python="python3"
alias pip="pip3"

echo "loaded."

