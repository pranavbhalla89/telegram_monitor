# telegram_monitor
Monitor for messages, photos on one or more telegram groups you're part of

This is a python script you can run on your local machine, that will send you alerts (through Telegram) when messages or photos are posted on some group you are interested in

Steps to get this running
- Goto https://my.telegram.org/, login with your phone number
- Goto API development tools, create a new application
- Save your api_id and api_hash to use in the [telegram_monitor.py](telegram_monitor.py)
- Install telethon `pip install telethon`

Things to note
- On the first run, the terminal will prompt you to enter your phone number (with the country code, e.g., +1234567890) and the login code that Telegram sends to your app
- Once logged in, it creates a session_monitor.session file. Next time you run the script, it will log in automatically without prompting you
- I've only tested it using the id for one particular group I was interested in (Id for groups are long negative numbers like -100123456789)
- Limited to one notification every 5 minutes per chat group being monitored (in case of message/photo storm)

Why build this
- I couldn't find a simple solution to monitor some large telegram groups I'm part of. I was using JunctionBot to do this previously but seems there isn't a free tier that did what I needed. There were some other bots out there but I was skeptical of sharing my credentials.

Built using Gemini
