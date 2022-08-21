### Instruction
### Create bot account go to URL =>
https://partners.viber.com/login?returnUrl=%2Faccount%2Fcreate-bot-account
### Input your API_KEY="".
### Expose your chat bot service to the internet.
### Command in terminal:
### Install ngrok and run him

```snap install ngrok ```

### Sign up account in Ngrok, copy authtoken and run next command

`sudo apt update && sudo apt upgrade`

`sudo apt install curl`

` ngrok config add-authtoken <token> `

` pip install viberbot `

` pip install flask `

``` ngrok http 8080 ``` or another port if you want.

### Insert url with terminal in file viber.json (example url: https://000-000-00-000-000.eu.ngrok.io )

*** When you every attempt run and stop and again command ngrok http 8080, every time change this url https://000-000-00-000-000.eu.ngrok.io and accordingly you must change him in file viber.json

### Run file app.py

`python3 app.py`

** Delete word TOKEN and input your auto-token with viber bot and run command

` curl -# -i -g -H "X-Viber-Auth-Token:ТОКЕН" -d @viber.json -X POST https://chatapi.viber.com/pa/set_webhook -v `

So, after that actions you can communicate echo-command with your viberbot in  viber.
