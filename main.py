import requests
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from src.pythonREPL import execute_python, install_package
import src.services as services
import json



app = Flask(__name__)

@app.route('/bot', methods=['GET'])
def bot():

    resp = MessagingResponse()
    msg = resp.message()

    incoming_msg = request.values.get('Body', '').strip()
    incoming_msg = incoming_msg.lower()    

    if incoming_msg.startswith('#!python3'):
        code = incoming_msg.strip('#!python3')
        output = execute_python(code)
        msg.body(output)
        

    elif incoming_msg.startswith('!pip install'):
        package = incoming_msg.split()[-1]
        output = install_package(package)
        msg.body(output)
        
    
    if 'your name' in incoming_msg:
        output = 'My name is PlanexBot'
        msg.body(output)

    elif 'what can i do here' in incoming_msg:
        output = '''
        This is the WhatsApp Bot that can allow you run a python code on it. 
        But! every python python code should start with #!python3
        because it's only compatible with python 3.x and newer'''
        msg.body(output)  

    elif 'joke' in incoming_msg:
        output = services.get_joke()
        msg.body(output)

    else:
        api_key = services.fetch_apikey('wolfram-alpha')
        if api_key == None:
            output = "wolram-alpha API key is required"
            msg.body(output)
        else:
            output = services.chatbot(api_key, incoming_msg)
            msg.body(output)
            my_dict = json.loads(output)
            
            for k in my_dict:
                if k == 'error':
                    output = my_dict[k]
                    msg.body(output)
                elif k == 'result':
                    output = my_dict[k]
                    msg.body(output)

            
           




    return str(resp)

if __name__ == '__main__':
    app.run()



