from pywebio.input import*
from pywebio.output import*
from pywebio import start_server
dol = 432
eur = 435
ghc = 42
def main():   
    def dollars(dols):
        result = dols * dol
        put_code("{:,} dollars is equal to {:,} NGN".format(dols,result),scope = "disp").style('width:70%; color:red;font-size: 24px;')
    def euros (euro):
        result = euro * eur
        put_code("{:,} Euros is equal to {:,} NGN" .format(euro,result),scope ="disp").style('width:70%; color:red;font-size: 24px;')
    def cedis(cd):
        result = cd * ghc
        put_code("{:,} Cedis is equal to {:,} NGN" .format(cd,result),scope ="disp").style('width:70%; color:red;font-size: 24px;')
         
    put_html("<h1>Currency Converter</h1>")
    put_html("<i><b>convert to Nigerian Naira</b></i>")
    put_scope("disp")
    while True: 
        options = radio("Choose Currency",["Dollar","Euro","Cedi"],inline = True, required=True)
        if options =="Dollar":
            resp = input("How many $:",type=NUMBER, onchange=lambda c :clear("disp"))
            dollars(resp)
            
        elif options == "Euro":
            resp = input("How many Euros:",type=NUMBER, onchange=lambda c :clear("disp"))
            euros(resp)
        elif options == "Cedi":
            resp = input("How many Cedis:",type=NUMBER, onchange=lambda c :clear("disp"))
            cedis(resp)
        
    #put_text("Hello World!")
if __name__ == '__main__':
    start_server(main, debug = True)
 