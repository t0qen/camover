import requests

# tags : https://docs.ntfy.sh/emojis/

def send_notif(title, data, priority, tags):
    requests.post("https://ntfy.rpi-server.org/camover-pi",
        data= data,
        headers={
            "Title": title,
            "Priority": priority,
            "Tags": tags
        })