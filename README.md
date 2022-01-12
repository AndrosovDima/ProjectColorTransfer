## This project is made to provide the color transfer from one photo/picture to another.
### Sometimes it can be useful to change the image style. The project can be used as the picture processing method, as the unique Instagram filter, etc.
# To up the project locally:

1. Clone the Git-repository. You can do this by running:
```
git clone https://github.com/AndrosovDima/ProjectColorTransfer.git
```

2. Complete the **Config.py** and **ConfigTelebot.py** files:
   - in the file **Config.py**:
     - rename variable *MAIL_USERNAME* by your ***Gmail login*** as ***username@gmail.com***
     - rename variable *MAIL_PASSWORD* by your ***Gmail password***
   - in the file **ConfigTelebot.py**:
     - rename variable *TOKEN* by your ***telegram-bot token***

3. To run the app and telegram-bot, you should run:
```
docker-compose up --biuld
```

# To use the existing running project:
### The project is already running on AWS. To use it you should:
- This site was built using [Link](http://44.201.126.187:5000/).
- You can also use only telegram-bot by using the [Telegram-Bot Link](https://t.me/ColorTransferBot).

# How to use the Color Transfer:
1. Choose the metric: the existing functional makes possible to use linear and quadratic metric. This metric is used to compare the distributions of pictures in RGB latent space to provide color transfer (quadratic is preferable).
2. Choose the file (photo/picture) to transfer color **TO**.
3. Choose the file (photo/picture) to transfer color **FROM**.
4. If you want to send the result by email, you should fill your Gmail login.
5. Finally, you can provide the color transfer in the following ways:
   - **Download** means transfer color and download the result picture.
   - **Transfer and show** means transfer color and show the result picture on the web-site.
   - **Send by message** means transfer color and send the result picture by the Email.

### The same functional is provided by the telegram-bot.