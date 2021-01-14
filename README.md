# OnlyFans-AutoLiker
![Python Version 3.8+](https://img.shields.io/badge/python-3.8-%2338AFF0)

A tool for automatically liking all of a user's posts on OnlyFans

<img src="https://raw.githubusercontent.com/Amenly/OnlyFans-AutoLiker/main/images/autoliker.gif">

# Preface
You know how sometimes there's OnlyFans creators who will message you saying something along the lines of: "Like all of my posts and I'll send you something special 😘"? Sometimes they might only have 20 or 30 posts, so it's not *too* bad. But what if they have *hundreds*? Maybe even ***thousands***? Well, this script will take of that for you.
 
# Installation
This tool only requires the [requests](https://github.com/psf/requests) library so if you already have it, you're good to go. Head on down to the [Configuration](#configuration) section!
 
Otherwise, run the following in your terminal:
```sh
$ pip3 install -r requirements.txt
```
 
# Configuration
In order to use this, you are going to need to fill out a few fields in the `auth.json` file. Those fields are:

```json
{
    "auth_id": "",
    "auth_uniq_": "",
    "sess": "",
    "user_agent": ""
}
```
*Note: you will only need to fill out* `auth_uniq_` *if you have 2FA (two-factor authentication) enabled*

If you're familiar with [DIGITALCRIMINAL's script](https://github.com/DIGITALCRIMINAL/OnlyFans), then great! All you have to do is copy the fields you filled out for that `auth.json` and paste them into this one! Now, you can go down to the [Usage](#usage) section.

If you're not, then don't worry; it's not hard to get them.

In order to get the proper values for those fields, open your web browser, go to OnlyFans, and make sure you're already logged in. Then, go to your 'Notifications' tab on OnlyFans and press the following keys to open your developer tools:

| Operating System | Keys |
| :----------------: | :----: |
| macOS | <kbd>alt</kbd><kbd>cmd</kbd><kbd>i</kbd> |
| Windows | <kbd>ctrl</kbd><kbd>alt</kbd><kbd>i</kbd> |
| Linux | <kbd>ctrl</kbd><kbd>shift</kbd><kbd>i</kbd> |

*Note: this table assumes you're using **Google Chrome** but this should work for other browsers as well, even **Safari***

Once you have the developer tools open, you need to click on the tab called `Network` and then click `XHR`:

<img src="https://raw.githubusercontent.com/Amenly/OnlyFans-AutoLiker/main/images/network-xhr-init.png">

Refresh the page if you don't see a field that starts with `init?app-token`. Once you see it, click on it and scroll down while in the `Headers` tab until you see a subsection called `Request Headers`. Inside of this subsection are two fields called `cookie` and `user-agent`. These are the two fields you need:

<img src="https://raw.githubusercontent.com/Amenly/OnlyFans-AutoLiker/main/images/cookie-user_agent.png">

Inside `cookie`, you should find your `sess` and `auth_id` cookies (as well as your `auth_uniq_` cookie if you have 2FA enabled). Copy their corresponding values and paste them into their corresponding spots in the `auth.json` file. Finally, copy what's next to the `user-agent` field and paste it into the `auth.json` file as well.

Your `auth.json` should look something like this:

```json
{
    "auth": {
        "auth_id": "1698967",
        "auth_uniq_": "",
        "sess": "yesny3cj2jku169pk0ked1g2p",
        "app_token": "33d57ade8c02dbc5a333db99ff9ae26a",
        "user_agent": "Mozilla/420.0 (Windows NT 420.0; Win420; x420) AppleWebKit/420.420 (KHTML, like Gecko) Chrome/420.420.420.420 Safari/420.420"
    }
}
```

But if you have 2FA enabled, then make sure the `auth_uniq_` field is filled.

Once that's all done, you're finally ready to use it!

# Usage
In order to use the script, run the following in your terminal:

```sh
$ python3 [ScriptName].py -u username [-w action]
```

Replace `username` with the username of the creator whose posts you want to like. 
Replace `action` with the action required. Use 'like' or 'unlike' (without quotes)
For example:

```sh
$ python3 autolikeunlike.py -u lenatheplugxxx
$ python3 autolikeunlike.py -u lenatheplugxxx -w like
^^ These two actions are identical ^^

$ python3 autolikeunlike.py -u lenatheplugxxx -w unlike

```

# Things to Note
1. The script runs a little quicker now.

The delay has been reduced from between 1 and 2.5 seconds to between 1 and 1.1 seconds.

2. Use it at your own risk

This kind of builds off of the first point. With the current speed, nothing bad should happen but I am ***not*** responsible for any unforeseen circumstances, whether good or unfortunate.

3. This does not process posts which are behind a paywall. That is, if a payment is required to unlock a post, that post will not be actioned by this script.

# Updates to To Do list from Amenly

* Posts actioned at a faster rate
* Option to unlike posts added via command line parameter

# Additional items incorporated
* Logging of actions to logfile with timestamps