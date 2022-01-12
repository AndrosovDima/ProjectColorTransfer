## This project is made to provide the color transfer from one photo/picture to another.
### Sometimes it can be useful to change the image style. The project can be used as the picture processing method, as the unique Instagram filter, etc.
# To up the project locally:
1. Install docker and docker-compose.

2. Clone the Git-repository. You can do this be running:
```
git clone https://github.com/AndrosovDima/ProjectColorTransfer.git
```

3. Complete the **Config.py** and **ConfigTelebot.py** files:
   - in the file **Config.py**:
     - rename variable *MAIL_USERNAME* by your ***Gmail login*** as ***username@gmail.com***
     - rename variable *MAIL_PASSWORD* by your ***Gmail password***
   - in the file **ConfigTelebot.py**:
     - rename variable *TOKEN* by your ***telegram-bot token***

4. To run the app and telegram-bot, you should run:
```
docker-compose up --biuld
```

# To use the existing running project:
### The project is already running on AWS. To use it you should:
- This site was built using [Link](http://44.201.126.187:5000/).
- You can also use only telegram-bot by using the [Telegram-Bot Link](https://t.me/ColorTransferBot).