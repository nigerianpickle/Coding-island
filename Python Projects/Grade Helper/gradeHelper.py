#Helps you to know your grade in a class
#Develped by Daniel Nwogo
#This program is a simple grade calculator that helps students calculate their GPA based on their grades and credit hours.
#It allows users to input their grades, credit hours, and current GPA to determine their overall GPA after a semester.
#The program also provides a function to calculate the total grade points based on the user's grades.
#It is designed to be user-friendly and provides clear instructions for inputting grades and credit hours.

import os
import random
import time


TOTAL_CREDIT_HOURS = 120  # Total credit hours required for graduation(Changes for some degrees)
CREDIT_HOURS=3 # Credit hours for each course(Changes for some degrees)

praiseTokens = ["Great job!", "Keep up the good work!", "You're doing amazing!", "Fantastic effort!", "You're on the right track!"]
bitterSweetTokens = ["You can do better!", "Don't give up!", "Keep pushing yourself!", "You're almost there!", "Stay focused!"]
meanTokens = ["You need to work harder!", "This is not acceptable!", "You can do much better!", "Don't let this bring you down!", "You need to improve!"]
snarkTokens = ["This is not good!", "You need to step up your game!", "This is disappointing!", "You can do much better than this!", "You need to take this seriously!"]

#This function will be used to help the user know their gpa
def helpUserGetGPA():
        print("How many courses have you taken?")
        courses=int(input("Enter the number of courses: "))
        i=courses
        
        totalGradePoints=0
        while courses>0:
            classGrade=input("Enter your"+ str(i)+" class grade: ")
            classGradePoint=getGradePoint(classGrade)
            totalGradePoints+=classGradePoint
            courses-=1
        
        
        currentGPA=totalGradePoints/courses
        print("Your current GPA is: ", currentGPA)
        print("Returining to main menu")

#Function to help return a valid grade point for a given grades
def getGradePoint(grade):
    validGrades = ['A+', 'A', 'B+', 'B', 'C+', 'C', 'D', 'F']
    if grade == 'A+':
        return 4.5
    elif grade == 'A':
        return 4.0
    elif grade == 'B+':
        return 3.5
    elif grade == 'B':
        return 3.0
    elif grade == 'C+':
        return 2.5
    elif grade == 'C':
        return 2.0
    elif grade == 'D':
        return 1.0
    elif grade == 'F':
        0.0
    else:
        print("Invalid grade")
        grade = input("Please enter a valid grade: ")
        while grade not in validGrades:
            grade = input("Please enter a valid grade: ")
        return getGradePoint(grade)
        
        
    
    




#Main execution of the program

done=False

while not done:
    answer=input("What would you like to do?\n1.Know your grade after a semester?\n2.Know your total grade points?\n3.Know how many classes you have left?\n4.Get advice on your grades?\nPress 0 to exit\n")
    if answer=="0":
        print("Exiting the program...")
        time.sleep(3)
        done=True
        break
        
    #To help the user know their grade after a semester
    if answer == "1":

        print("What is your current GPA? If you don't know it, please enter 0")
        currentGPA=float(input("Enter your current GPA: "))
        if(currentGPA==0):
            helpUserGetGPA()
        else:
            print("How many courses have you taken in total(Apart from this semester)(This is total credit hours / 3)?")
            totalcourses=int(input("Enter the total number of courses: "))
            
            print("How many courses did you take this semester?")
            courses=int(input("Enter the number of courses: "))
            prevTotal=totalcourses
            totalcourses=totalcourses+courses
            i=1
            totalGradePoints=0
            while courses>0:
                classGrade=input("Enter your"+" class"+ str(i)+" grade: ")
                classGradePoint=getGradePoint(classGrade)
                totalGradePoints+=classGradePoint
                i+=1
                courses-=1
            
            currentTotalGradePoints=(currentGPA*prevTotal)+totalGradePoints
            
            
            currentGPA=currentTotalGradePoints/totalcourses
            print("Your current GPA is: ", currentGPA)
            print("Returining to main menu")
            time.sleep(3)
                
        #To help the user know their total grade points
    elif answer=="2":
        helpUserGetGPA()
    elif answer=="3":
        currentHour=int(input("Enter your current credit hours: "))
        hoursLeft=TOTAL_CREDIT_HOURS-currentHour
        
        if hoursLeft>0:
            print("You have",hoursLeft,"credit hours left to graduate")
            print("You have",hoursLeft//CREDIT_HOURS,"classes left to graduate")
            
        elif hoursLeft==0:
            print("You have no credit hours left to graduate")
        else:
            print("You have exceeded the total credit hours required for graduation by",abs(hoursLeft),"credit hours")
            
        
        print("Returining to main menu")
        time.sleep(3)

    elif answer=="4":
        #Funniest part of the program
        gpa=float(input("Enter your current GPA: "))
        if gpa>=4.0:
            print("You are doing great!")
            pool=(praiseTokens,bitterSweetTokens)
            print(random.choice(random.choice(pool)))
            
        elif gpa>=3.0:
            print("You are doing good!")
            pool=(praiseTokens,bitterSweetTokens)
            print(random.choice(random.choice(pool)))
        elif gpa>=2.0:
            print("Hmm!")
            pool=(bitterSweetTokens,meanTokens)
            print(random.choice(random.choice(pool)))
        elif gpa>=1.0:
            print("You need to work harder!")
            pool=(meanTokens,snarkTokens)
            print(random.choice(random.choice(pool)))
            
            
        time.sleep(3)
            
    
    
    
