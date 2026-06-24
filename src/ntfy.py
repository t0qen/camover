import requests

# tags : https://docs.ntfy.sh/emojis/

def send_notif(title, data, priority, tags):
    try:
        requests.post("http://192.168.1.23:8061/camover-pi",
            data= data,
            headers={
                "Title": title,
                "Priority": priority,
                "Tags": tags
            })
    except Exception as e:
        print(e)
