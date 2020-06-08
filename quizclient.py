import socket
import time as t
from threading import Thread
import datetime


HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))                                              #Connection established.

    message = s.recv(1024).decode('utf-8')                              #Initial message recieved from server.
    print(message)                                                      #Prints initial message.
    
    answer = input('Username:')                                         #Username is taken from User by client.
    s.sendto(answer.encode('utf-8'), (HOST, PORT))                      #And sent to server.

    message = s.recv(1024).decode('utf-8')                              #Informative message is taken.
    print(message)                                                      #Printed.

    choice = input('Choice:')                                           #Choice is taken from user by client.
    s.sendto(choice.encode('utf-8'), (HOST, PORT))                      #And sen to server.

    message = s.recv(1024).decode('utf-8')                              #Response taken from server.
    print(message)                                                      #Printed.
    t.sleep(2)                                                          #To give a read time to user.


    while True:
        tim = datetime.datetime.now()                                   #Used to take current date to inform user.
        now = t.time()  
        endt = now + 60
        inputstr = 'Time: ' + str(tim.hour) +":"+ str(tim.minute) +":"+ str(tim.second) + ' give your answer in 1 minute:'       
        message = s.recv(1024).decode('utf-8')                          #Questions and options is taken from server.
        print(message)                                                  #And printed.

        if message[0:4] == "Quiz":                                      #If message starts with Quiz it means Quiz is over. Expects q to close client.
            answer = input('Type (q) to quit: ')
            if answer == "q":
                s.close()
                exit(0) 

        answer = input(inputstr)                                        #Answer input is taken from user.

        if (t.time() > endt):                                           #If time is up answer is taken as z which is always incorrect then passes to next question
            tim = datetime.datetime.now()
            print('Time: ' + str(tim.hour) +":"+ str(tim.minute) +":"+ str(tim.second) + ' your answer will not count.')
            answer = "z"
            s.sendto(answer.encode('utf-8'), (HOST, PORT))
            t.sleep(2)                                                      #To give a read time to user.
            continue
    
        try:
            if answer == "q":                                           #Closes if a q is recieved.
                s.close()
                exit(0)            
            else:
                tim = datetime.datetime.now()
                print('-> ' +answer + ' is your answer. Time: ' +  str(tim.hour) +":"+ str(tim.minute) +":"+ str(tim.second))               #Any other input is taken as answer.
                s.sendto(answer.encode('utf-8'), (HOST, PORT))
                t.sleep(2)                                                      #To give a read time to user.
                
        except:
            s.close()
            exit(0)


    