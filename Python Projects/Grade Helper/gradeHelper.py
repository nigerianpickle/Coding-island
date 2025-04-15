#Helps you to know your grade in a class


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
answer=input("What would you like to do?\n1.Know your grade after a semester?\n2.Know your total grade points?\n3.Know how many classes you have left?\n4.Get advice on your grades?")


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
        
#To help the user know their total grade points
