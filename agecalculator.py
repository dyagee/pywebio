#import the necessary modules(pywebio,datetime, start_server and re)

from pywebio.input import*
from pywebio.output import*
from pywebio import start_server
from datetime import datetime
import re
#Header of the page and little description
def main():
    put_html("<h1>AGE CALCULATOR</h1>").style("text-align:center;")
    put_html("<i><b>check age in just few clicks...</b></i>")
    put_scope("disp")
    while True:
        ny= input("Current Year(yyyy):",type=NUMBER, onchange=lambda c :clear("disp"));mn= input("Current month:",type=NUMBER, onchange=lambda c :clear("disp"));dn= input("Day:",type=NUMBER, onchange=lambda c :clear("disp"))
        yr= input("Year of Birth(yyyy):",type=NUMBER, onchange=lambda c :clear("disp"));mm= input("Month of Birth:",type=NUMBER, onchange=lambda c :clear("disp"));dd= input("Day:",type=NUMBER, onchange=lambda c :clear("disp"))
        nw = datetime(ny,mn,dn)
        dob=  datetime(yr,mm,dd)
        tdelta = str(nw-dob) #convert the timedelta to string
        diff = re.findall(r"\d+\s",tdelta) #extract only the number of days from the timedelta
        diff = diff[0].strip()   #remove and white spaces and then convert to years by /365
        diff = int(diff)/365
        result = "You're {:.1f} years old".format(diff)
        put_code(result,scope ="disp").style('width:70%; color:green;font-size: 24px;')
    

if __name__ == '__main__':
    start_server(main, debug = True)

