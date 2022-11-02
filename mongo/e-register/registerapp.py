#This is simple but multifunctional E-register based of python and Mongodb
#*****************************************************************************************************
#*************************************LICENCE AGREEMENT***********************************************
#*****************************************************************************************************
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

#import all the modules
from pywebio.input import*
from pywebio.output import*
from pywebio import start_server,config
from registerFunctions import*
import datetime
import random as r
__version__ = "1.0"
__author__ = "A. Agee"


#configure the some styling
config(theme='dark')
#create a background scope and keep as a bgroung function
put_html('''<head>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    </head>''')
def bground(): 
    put_scope("background").style("padding-top:5px;padding-bottom:5%; border-radius:20px; background: rgb(84,121,128);background: linear-gradient(0deg, rgba(84,121,128,1) 32%, rgba(45,150,152,1) 49%, rgba(153,153,153,1) 69%, rgba(47,149,153,1) 89%);")
    #Title header font-awesome icons
    put_html("<i class='fa fa-users'></i><i class='fa fa-users'></i><br/>",scope="background").style('''text-align:center;width:auto;font-size:56px; opacity:0.4;z-index:100;border-radius:100%;background: rgb(167,224,235);
    position:relative; margin:3%; background: linear-gradient(0deg, rgba(167,224,235,0.7567401960784313) 16%, rgba(165,231,232,0.5242471988795518) 49%, rgba(134,228,221,0.6558998599439776) 69%, rgba(23,205,212,0.6474964985994398) 95%);''')
    with use_scope("background"):
        
        #create a center div
        now = datetime.datetime.now()
        if (now.strftime("%p").lower() == "am"):
            greeting = "good morning"
        if (now.strftime("%p").lower() == "pm") and int(now.strftime("%I")) < 4:
            greeting = "good afternoon"
        if (now.strftime("%p").lower() == "pm") and int(now.strftime("%I")) >= 4:
            greeting = "good Evening"
        #above lines, fetches current time and determine the welcome greeting string
        #the section below, is the heading of the app, with linebreaks and call to action buttons 
        put_html("Hi, {} Dear! <br/> Welcome To Class".format(greeting)).style("text-align:center;font-weight:500px; font-style:bold;font-size:30px;color:#ffffff;")
        put_scope("centered").style("")
        with use_scope("centered"):
            #create the call to action buttons
            put_html("<br/><br/><br/>")
            put_button("Enroll Teacher", onclick= lambda: teacherSection() ).style("position:relative; left:43%;")
            put_html("<br/><br/>")
            put_button("Enroll Student", onclick= lambda: studentSection() ).style("position:relative; left:43%;")
            put_html("<br/><br/>")
            put_button("Attendance", onclick= lambda: attendance() ).style("position:relative; left:44%;")
            put_html("<br/><br/>")

#section for teacher enrollment
def teacherSection():
    #first thing clear the background, and put out input form
    remove("centered")
    remove("register")
    code = r.randrange(2001,2500)
    info = input_group('Add user', [
    input('Name', type=TEXT, name='name', required=True, placeholder='Enter Name'),
    input('Department', type=TEXT, name = 'dept', required=True, placeholder='Enter department')], cancelable=True)
    
    if info is not None: #verify that empty fields aren't submitted
        teacherEnroll(info['name'],code,info['dept'])
        toast("%s  ID: %d Added Successfully!"%(info['name'],code),position='right', color='primary',duration=6)
    remove("background") # this is to prevent "Error: The name of this scope is duplicated with the previous one!"
    bground()

#functions for marking attendance, both seems the same 
#few key differences with regards to being present or Absent
def present(name,attendance):
    confirm = students.find_one({'name':name},{'_id':0,'present':1})
    confirm2 = students.find_one({'name':name},{'_id':0,'absent':1})
    val =confirm['present']
    val2 = confirm2['absent']
    #condition to avoid multiple marking per day
    if attendance not in val and attendance not in val2:
        students.update_one({'name':name},{'$push':{'present':attendance}})
        i = students.find_one({'name':name},{'_id':0,'present':1})
        dayspresent =i['present']
        students.update_one({'name':name},{'$set':{'daysPresent':len(dayspresent)}})
        #put_text(len(dayspresent),scope="background")
    else:
        put_error("Attendance already marked for the day",scope="background",closable=True)
        scroll_to("background",position="bottom")

def absent(name,attendance):
    confirm = students.find_one({'name':name},{'_id':0,'absent':1})
    confirm2 = students.find_one({'name':name},{'_id':0,'present':1})
    val =confirm['absent']
    val2 = confirm2['present']
    #condition to avoid multiple marking per day
    if attendance not in val and attendance not in val2:
        students.update_one({'name':name},{'$push':{'absent':attendance}})
        k = students.find_one({'name':name},{'_id':0,'absent':1})
        daysabsent = k['absent']
        students.update_one({'name':name},{'$set':{'daysAbsent':len(daysabsent)}})
    else:
        put_error("Attendance already marked for the day",scope="background",closable=True)
        scroll_to("background",position="bottom")

#section for students enrollment
def check_form(data):
    if data['age'] > 27:
        return ('age', 'Age above requirement!')
    if data['age'] < 8:
        return ('age', 'Age below requirement')
    if len(data['class']) > 3:
        return ('class','Enter correct format')
def studentSection():
    #first thing clear the background, and put out input form
    remove("register")
    remove("centered")
    code = r.randint(1001,1500)
    info = input_group('Add Student', [
    input('Name', type=TEXT, name='name', required=True, placeholder='Enter full Name'),
    input('Age', type=NUMBER, name = 'age', required=True, placeholder='Enter age (8-27)'),
    input('Class', type=TEXT, name='class', required=True, placeholder='Enter class e.g 12A, 7B'),
    input('State of Origin', type=TEXT, name='state', required=True, placeholder='Enter State'),
    input('Role', type=TEXT, name='role', required=True, placeholder='Enter role or just write Student')],
    cancelable=True,validate=check_form)
    
    if info is not None: #verify that empty fields aren't submitted
        studentsEnroll(info['name'],info['age'],code,info['class'], info['state'],info['role'])
        toast("%s  ID: %d  in Class: %s Added Successfully!"%(info['name'],code,info['class']),position='right', color='primary',duration=6)
    
    remove("background") # this is to prevent "Error: The name of this scope is duplicated with the previous one!"
    bground()
    

#section for marking attendance
def attendance():
    remove("register")
    classlist = students.find({},{"_id":0,"name":1,"id":1}).sort("name")

    #below is to enable us use font-awesome icons in our app
    
    with use_scope("background"):
        put_scope("register").style('''background: rgb(58,168,189);
        background: linear-gradient(0deg, rgba(58,168,189,1) 16%, rgba(44,207,210,0.5242471988795518) 49%, rgba(153,153,153,0.6558998599439776) 69%, rgba(23,205,212,1) 95%);
        color:#0D2C4C;text-align:justify; padding:0.85em;position:relative;left:10%;border-radius:10px;
        width:80%;
        ''')
        with use_scope("register"):
            #timeStamp = datetime.datetime.now().strftime("%d"+"/"+"%m"+"/"+"%Y"+"-"+"%I"+":"+"%M"+ "" + "%p")
            timeStamp = datetime.datetime.now().strftime("%d"+"-"+"%m"+"-"+"%Y")
            #attendance serial numbering
            SN = 1 
            #attendance list header row
            put_row([put_code('S/N'),put_code('Name'),put_code("ID"),put_code('timeStamp'),put_code('status')],size='10% 35% 12% 18%  26%')
            for student in classlist:
                #outputs each student on a seperate row with the corresponding field and spacing 
                put_row([put_code(SN),put_code(student['name']),put_code("["+ str(student['id'])+"]"),put_code(timeStamp),None,put_button("present", color= 'dark',onclick=lambda a=student['name'],b=timeStamp:present(a,b)),None,put_button("absent", color= 'dark',onclick=lambda c=student['name'],d=timeStamp:absent(c,d))],size='10% 35% 12% 18% 10px 10% 20px 10%')
                #put_buttons([put_html("<i class = 'fa fa-check-square-o'> Present</i>"),None,put_html("<i class ='fa fa-close' > Absent </i>")]))
               
                SN += 1
        scroll_to("register",position='middle')
    
bground()
