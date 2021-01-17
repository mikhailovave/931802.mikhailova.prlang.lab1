from wsgiref.simple_server import make_server
from wsgiref import util
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timezone, timedelta
import json

#Нужно установить библиотеки pytz и tzlocal с помощью pip install
import pytz
from tzlocal import get_localzone

#Список всех доступных тайм зон
all_tz = pytz.all_timezones

status_ok = "200 OK"
status_bad = "400 BAD REQUEST"

def get_time(tz):
    return None if tz not in all_tz else datetime.now(tz=pytz.timezone(tz))

def parse_time(string):
    try:
        try: 
            return datetime.strptime(string, '%m.%d.%Y %H:%M:%S')
        except:
            return datetime.strptime(string, '%H:%M%p %Y-%m-%d')
    except:
        return None

def app(environ, start_response):
    method = environ['REQUEST_METHOD']
    url = util.request_uri(environ)
    path = urlparse(url).path

    status = status_bad
    content = ""
    #Запрос к странице
    
    if method == "GET":
        headers = [('Content-type', 'text/html; charset=utf-8')]

        tz = '/'.join(path.split('/')[1:]) or str(get_localzone())
        time = get_time(tz)

        if time:
            status = status_ok
            content = html_response(
                str(time.tzinfo),
                time.strftime('%Y-%m-%d %H:%M:%S')
            )

    #Запрос к API
    elif method == "POST":
        headers = [('Content-type', 'application/json; charset=utf-8')]

        try:
            content_length = int(environ["CONTENT_LENGTH"])
        except:
            content_length = 0

        try:
            req_obj = json.loads(environ["wsgi.input"].read(content_length) or "{}")
            if path == "/api/v1/time":
                tz =  req_obj["tz"] if "tz" in req_obj else str(get_localzone())
                time = get_time(tz) 
                if time:
                    status = status_ok
                    content = json.dumps({
                        "tz": tz,
                        "time": time.strftime('%H:%M:%S')
                    })
            

            elif path == "/api/v1/date":
                tz = req_obj["tz"] if "tz" in req_obj else str(get_localzone())
                time = get_time(tz)

                if time:
                    status = status_ok
                    content = json.dumps({
                        "tz": tz,
                        "date": time.strftime('%Y-%m-%d')
                    })

            elif path == "/api/v1/datediff":
                start = parse_time(req_obj["start"]["date"])
                end = parse_time(req_obj["end"]["date"])

                tz1 = pytz.timezone(req_obj["start"]["tz"]) if "tz" in req_obj["start"] else get_localzone()
                tz2 = pytz.timezone(req_obj["end"]["tz"]) if "tz" in req_obj["end"] else get_localzone()
                
                start = tz1.localize(start)
                end = tz2.localize(end)

                diff = end - start

                status = status_ok
                content = json.dumps({"diff": str(diff)})

        except:
            pass
        
        
    #Отправка ответа
    start_response(status, headers)
    return [row.encode() for row in content]


def html_response(tz, time):
    return """
    <body>
        <h2>{tz}</h2>
        <time>{time}</time>
    <body>
    """.format(tz = tz, time = time)


# Запуск wsgi сервера
httpd = make_server('', 8080, app)
print("Serving on port 8080...")
httpd.serve_forever()