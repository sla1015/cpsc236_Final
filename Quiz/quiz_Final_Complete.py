import sys
import csv
import random
import time
import os


def main():
    
    # Gets the Users Name and ID, input validates, and exits the program if that fails thrice. Lines 13-16 done by Sage
    firstName, lastName, idNum = getUser()
    if firstName == '0':
        sys.exit()
    
    
    questions, elapsed, score = startQuiz() # Keeps track of the questions, elapsed time, and the score. Sage
    
    writeFile(firstName, lastName, idNum, questions, elapsed, score) # Writes the name and ID, along with the questions time and score to a file. Sage

    
    # Gives the user the option to exit the quiz or start over. Lines 24-32 by Seth
    choice=input("Enter Q to exit or S to clear the screen and start a second quiz: ")
    while choice.upper() !='Q' and choice.upper() !='S':
        choice=input("incorrect response; Enter Q to exit or S to clear the screen and start a second quiz: ")
    if choice.upper()=='Q':
        sys.exit()
    elif choice.upper() == 'S':
        os.system('cls')
        main()



def startQuiz():
    """
    Parameters
    ----------
    NONE
    
    Returns
    -------
    questions : LIST
        The list of questions printed to the user.
    elapsed : INT
        Amount of time elapsed during the testing process.
    score : INT
        The user the score recieved.
    
    Function
    --------
    Prompts the user on how many questions they would like and then initiates the quiz loop.
    
    Authored
    --------
    Fully written by Seth
    """
   
    quizLength=int(input("Would you like 10 or 20 Questions? "))
    
    while quizLength != 10 and quizLength != 20:
        quizLength=int(input("Invalid Response. 10 or 20 Questions? "))
    
    questions, elapsed, score = quizLoop(quizLength=quizLength)
    
    return questions, elapsed, score

def quizLoop(quizLength):
    """
    Parameters
    ----------
    quizLength : INT
        Tells the quizLoop how many questions to administer
    
    Returns
    -------
    questions : LIST
        The list of questions printed to the user.
    elapsed : INT
        Amount of time elapsed during the testing process.
    score : INT
        The user the score recieved.
    
    Function
    --------
    Reads the text bank to a list of dictionaries, keeps track of time elapsed, and tracks the questions administered, guesses made, and correct answers.
    
    Authored
    --------
    Seth : 95-99 , 103-127 , 137-139
    Sage : 100-102 , 129-134 , 141-142
    """
    wrong=0
    right=0
    with open('testBank.csv', 'r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)
        testBank = [row for row in csv_reader]
    questions=[]
    
    tempDict = {}
    start=time.time()
    chosen=[]
    for i in range(quizLength):
        if time.time()-start>600:
            break
        else:
            x=random.randrange(len(testBank))
            while x in chosen:
                x=random.randrange(len(testBank))
                print("OOPS WE ALREADY HAVE QUESTION",x,'\n')
            chosen.append(x)
            
            print("Question number ",x,':\n',testBank[x]["Question text"],sep='')
            print("A: ",testBank[x]["Option A"],sep='')
            print("B: ",testBank[x]["Option B"],sep='')
            print("C: ",testBank[x]["Option C"],sep='')
            
            guess=input("Answer: ")
            
            while guess.upper() != 'A'and guess.upper() !='B'and guess.upper() !='C':
                guess=input("Invalid Response, Guess Again: ")
            if guess.upper() != testBank[x]["Correct Answer"]:
                wrong+=1
            else:
                right+=1
            
            tempDict = {}
            
            tempDict['question'] = (str(x) + ' ' + testBank[x]['Question text'])
            tempDict['user answer'] = guess.upper()
            tempDict['correct answer'] = testBank[x]['Correct Answer']
            questions.append(tempDict)
    
    
    end=time.time()
    elapsed=round(end-start,3)
    print("TOTAL TIME =",elapsed)
    
    score = evaluate(right=right,wrong=wrong,quizLength=quizLength)
    return questions, elapsed, score
    
def evaluate(right,wrong,quizLength):
    """
    
    Parameters
    ----------
    right : INT
        Number of questions gotten right.
    wrong : INT
        Number of questions gotten wrong.
    quizLength : INT
        NUmber of questions administered.

    Returns
    -------
    score : INT
        Score recieved.
        
    Function
    --------
    Recieves the amount of questions, right, and wrong and then calculates a score from that
    
    Authored
    --------
    Seth 169-171
    Sage 175
    """
    score=(right/quizLength)*100
    print("You got",right,"correct and",wrong,"incorrect")
    print("Your score is",score,"%")
    
    return score
    

def getUser():
    """
    Parameters
    ----------
    NONE
    
    Returns
    -------
    firstName : STRING
        The users first name
    lastName : STRING
        The users last name
    idNum : STRING
        The users Id
    
    Function
    --------
    Accepts the Users first and last name and their ID. gives them three tries to get it right and if they get it wrong
    three times exits the program. Ensures that the ID involves a capital A and 6 digits between 1 and 9
    
    Authored
    --------
    Fully authored by Sage
    """

    firstName = input("Enter first name: ")
    lastName = input("Enter last name: ")
    idNum = input("Enter your ID: ")
    count = 1
    invalidID = idNum[0] !='A' or len(idNum) > 6 or len(idNum) < 6 or '0' in idNum
    while invalidID and count < 3:
        idNum = input('Invalid ID. Try again: ')
        invalidID = idNum[0] !='A' or len(idNum) > 6 or len(idNum) < 6 or '0' in idNum
        count += 1
    if invalidID and count == 3:
        return '0','0', '0'
    else:
        return firstName, lastName, idNum
    
def writeFile(first, last, num, questions, elapsed, score):
    """
    Parameters
    ----------
    first : STRING
        The users First Name.
    last : STRING
        DESCRIPTION.
    num : STRING
        The users Last Name.
    questions : LIST
        The list of questions printed to the user.
    elapsed : INT
        Amount of time elapsed during the testing process.
    score : INT
        The user the score recieved.
    
    Returns
    -------
    NONE
    
    Function
    --------
    Accepts all the arguments and writes them to a file with the proper formatting
    
    Authored
    --------
    Fully authored by Sage
    """
    
    fileName = num + "_" + first + "_" + last + '.txt'
    with open(fileName, 'a', newline = '') as file:
        file.write(num + ' ' + first +  ' ' +  last + "\n")
        file.write("Score:" + str(score) + "\n")
        file.write("Time elapsed:" + str(elapsed) + "\n")
        for question in questions:
            file.write('\n' + question['question'] + "\n")
            file.write("User Answer: " + question['user answer'] + "\n")
            file.write("Correct Answer: " + question['correct answer'] + "\n")
        

if __name__ == "__main__":
    main()
