print("Welcome to my computer quiz")

playing = input("Do you want to play? ")
if playing.lower() != "yes":
    quit()

print("Ok Lets play!!!")
score = 0

answer = input("What is CPU stand for ")
if answer.lower() == "central processing unit":
    print("Correct")
    score += 1

answer = input("What is GPU stand for ")
if answer.lower() == "graphics processing unit":
    print("Correct")
    score += 1
else:
    print("Incorrect") 

answer = input("What is PSU stand for ")
if answer.lower() == "power supply":
    print("Correct")
    score += 1
else:
    print("Incorrect") 

answer = input("What is RAM stand for ")
if answer.lower() == "random access memory":
    print("Correct")
    score += 1
else:
    print("Incorrect") 

print ("You got " + str(score) + " questions")
print ("You got " + str((score/4)*100) + "%" )