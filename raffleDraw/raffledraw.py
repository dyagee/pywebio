
from pywebio.input import*
from pywebio.output import*
import time
import random as r


def raffledraw():
    try:
        put_scope("mainframe").style("background: linear-gradient(to right, #536976, #292e49);border-radius:8px;opacity:0.6;") #this serves as app background
        with use_scope("mainframe"):
                #show Header of the app 
                put_html("<h1>Online Raffle Draw Engine</h1>").style("text-align:center;color:#ffffff; font-style:bold;") 
                put_html("<h5>....thousands but only 1 lucky winnner!</h5><br/><br/>").style("text-align: center;color:#ffffff;")  
                put_button("Click Here", onclick= lambda: inpts() ).style("position:relative; left:45%;")

        def inpts():
                #Let's resets every input and out first.
                remove("body2")
                remove("disp")
                remove("err")
                x =0
                y =0
                x = input("Enter Lowest",type=NUMBER, required=True,placeholder="enter a number")
                y = input("Enter Highest",type=NUMBER, required=True,placeholder="enter a number")
                result = r.randint(x,y)
                put_scope("body2").style("width:80%; position:relative; left:10%;background:#292e49;border:none; border-radius:10px;")#this scope is for output
                if result>=1:
                    with use_scope("body2"):  
                                    put_scope("disp").style("position:relative; left;30%; width:50%;color:#ffffff;border-left-radius:10px;")
                                    with use_scope("disp"):    
                                        with put_loading(shape="grow",color="success"):
                                            time.sleep(7)
                                            put_code("Lucky winner {}".format(result)).style("border-left:1px solid #292e49; color:#66BF34; font-size:24px;font-style:bold;")
                
                    
    except:
        put_scope("err").style("width:80%; position:relative; left:10%;background:#292e49;border:none; border-radius:10px;")
        put_warning("A fatal ERROR OCCURED Please close this window and Restart the APP").style("color:red; font-size:300px;")

#this start server when running a local machine, it should be uncommented
#if __name__ == "__main__":
#    start_server(raffledraw,port=8080,debug=True)

#below section for when running app on cloud platform
if __name__ == '__main__':
    import argparse
    from pywebio.platform.tornado_http import start_server as start_http_server
    from pywebio import start_server as start_ws_server

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    parser.add_argument("--http", action="store_true", default=False, help='Whether to enable http protocol for communicates')
    args = parser.parse_args()

    if args.http:
        start_http_server(raffledraw, port=args.port)
    else:
        # Since some cloud server may close idle connections (such as heroku),
        # use `websocket_ping_interval` to  keep the connection alive
        start_ws_server(raffledraw, port=args.port, websocket_ping_interval=30)