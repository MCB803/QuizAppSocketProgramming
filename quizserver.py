import socket
import threading
import time
import json
import random

HOST = '127.0.0.1'
PORT = 65432

class QuizServer():
    def listenClient(self, client, address):
        a = 0
        while a==0:                                                                         #To prevent taking quiz over and over.
            initMsg = "Welcome to the Quiz. Type q to quit quiz."
            client.sendto(initMsg.encode('utf-8'), (HOST, PORT))                            #Initial message sent to client.
            username = client.recv(1024).decode('utf-8')                                    #Username is taken from client and stored.

            with open('C:\\Users\\Mert\\Desktop\\networkhw\\ServerCode_data_questions.json', encoding='utf-8') as f: #JSON File opened.
                
                data = json.load(f)                                                         #Stored as a dictionary here.
                points = 0                                                                  #Quiz points.

                userMsg = "Welcome " + username + "! \nFor " + data[0]['content'] + " quiz, type (g) \nFor " + data[16]['content'] + " quiz, type (l)" #Quiz Type option.
                client.sendto(userMsg.encode('utf-8'), (HOST, PORT))                        #Quiz types sent to client.

                quizType = client.recv(1024).decode('utf-8')                                #Desired quiz type is taken from client.
                if(quizType == "g"):                                                        #Quiz type 'Game of Thrones'
                    userMsg2 = "Game of Thrones Quiz is selected.\nYou have 1 minute to answer each question.\nAfter 1 minute you won't get any points for any answer. Good Luck!" #Informative text.
                    client.sendto(userMsg2.encode('utf-8'), (HOST, PORT))                   #Sent to client.

                    randlist = random.sample(range(16), 5)                                  #To prevent duplicate questions. 5 Different rand question number is taken. 0-16 Questions are GoT Questions
                    for i in randlist:                                                      #Loop through questions.
                        questionStr = data[i]['question'] + "\n a) " + data[i]['a']  + "\n b) " + data[i]['b']  + "\n c) " + data[i]['c']  + "\n d) " + data[i]['d'] #Question and options.
                        client.sendto(questionStr.encode('utf-8'),(HOST, PORT))             #Sent to client.
                        answer = client.recv(1024).decode('utf-8')                          #Answer is taken from client and stored.

                        if answer.lower() == data[i]['answer']:                             #If answer is correct then adds 20 points to user.
                            points += 20
                elif(quizType == "l"):                                                      #Quiz type 'Lord of the Rings'
                    userMsg2 = "Lord of the Rings Quiz is selected.\nYou have 1 minute to answer each question.\nAfter 1 minute you won't get any points for any answer. Good Luck!"  #Informative text.
                    client.sendto(userMsg2.encode('utf-8'), (HOST, PORT))                   #Sent to client.

                    randlist = random.sample(range(16,30), 5)                               #To prevent duplicate questions. 5 Different rand question number is taken. 16-30 Questions are LotR Questions
                    for i in randlist:                                                      #Loop through questions.
                        questionStr = data[i]['question'] + "\n a) " + data[i]['a']  + "\n b) " + data[i]['b']  + "\n c) " + data[i]['c']  + "\n d) " + data[i]['d']  #Question and options.
                        client.sendto(questionStr.encode('utf-8'),(HOST, PORT))             #Sent to client.
                        answer = client.recv(1024).decode('utf-8')                          #Answer is taken from client and stored.

                        if answer.lower() == data[i]['answer']:                             #If answer is correct then adds 20 points to user.
                            points += 20
                else:                                                                       #If either l or g not entered. Then restarts the client.
                    userMsg2 = "Invalid Input. Please try again."
                    client.sendto(userMsg2.encode('utf-8'), (HOST, PORT))
                    continue
            a = a+1         
            
        print(username, " points: ", str(points))                                           #Prints total points to server console.
        pointstr = "Quiz is over. Points: " + str(points)                                   
        client.sendto(pointstr.encode('utf-8'),(HOST, PORT))                                #Sends total points to client.

    def __init__(self, serverPort, serverName):

        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                    #Socket is initialized and created.
        print("Socket is created.")

        serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)                  #Socket is in use.
        print("Socket is in use.")

        serverSocket.bind((serverName, serverPort))                                         #Binding
        print("Binding is completed.")

        serverSocket.listen(45)                                                             #Now server listening clients.
        print("Server is listening now.")

        while True:
            connectionSocket, addr = serverSocket.accept()                                  #Socket connection and address taken.

            threading.Thread(target=self.listenClient, args=(connectionSocket, addr)).start()       #To deal with multiple clients, we need to use threads.

if __name__ == "__main__":                                                                   #Main Function.
    QuizServer(PORT, HOST)

