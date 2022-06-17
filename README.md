# discord-bot-lua-obfuscator (python 3.7.9)

# Live Preview: https://discord.gg/STaq3UDbqQ
<img src="https://i.imgur.com/DlO9XIa.png">

 


# Original code: https://github.com/yunglean4171

Simple discord bot written in python for obfuscating lua files sent by a user in a specific channel (also works in direct messages). 
Useful for securing your lua scripts (work with fivem/roblox etc resources).

```
This is a modified version for repl and heroku.

In repl start a blank template and import from github.com. https://github.com/jmesfo0/discord-bot-lua-obfuscator 
In repl put DISCORD_TOKEN in system environment variables.
In repl shell type chmod +x bin/* to allow lit luvi & luvit to be executed.
Enjoy your free private obfuscator.
```

## Required python modules:
- Discord.py 
- requests
- Flask



## Heroku Guide

Fork this repoistory.<br />
Create an app on Heroku.<br />
Select Deploy->Github and connect your account.<br />
Put repo name in.<br />
Select Enable Automatic Deploys then Deploy Branch<br />
Go to Settings->Reveal Config Vars<br />
Add DISCORD_TOKEN in environmental variables.<br />
Done.
