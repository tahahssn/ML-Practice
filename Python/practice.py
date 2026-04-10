# unit = input("Enter The Unit of temperature (C/F): ")
# temp = float(input("Enter the Temperature: "))

# if unit == "C":
#     temp = ((9 * temp)/5 + 32)
#     print(f"The temperature in farehiet is: {temp}")
# elif unit == "F":
#     temp = ((temp - 32) * 5/9)
#     print(f"The temperature in Calcius is: {temp}")
# else:
#     print(f'{unit} is not valid!')

#PYTHON COMPOUND INTEREST CALCULATOR

# principle = 0
# rate = 0
# time = 0
# while True:
#     principle = float(input("Enter Your Pricniple Amount: "))
#     if principle < 0:
#         print("Principle can be less than and equalo to zero!")
#     else:
#         break

# while True:
#     rate = float(input("Enter Your Rate Amount: "))
#     if rate < 0:
#         print("Rate can be less than and equalo to zero!")
#     else:
#         break

# while True:
#     time = int(input("Enter Time In Years: "))
#     if time < 0:
#         print("Rate can be less than and equalo to zero!")
#     else:
#         break

# total = principle * pow((1 + rate/100), time)
# print(f"Balance after {time} years/s: ${total:.2f}")

# COUNTDOWN TIMER PROGRAM

# import time

# mytime = int(input("Enter Time In Seconds: "))
# print("CountDown Started")

# for x in range(mytime, 0, -1):
#     second = x % 60
#     minutes = int((x/60) % 60)
#     hours = int((x / 3600) % 24)
#     print(f"{hours:02}.{minutes:02}.{second:02}")
#     time.sleep(1)

# print("Time's Up")

# NESTED LOOPS

# rows = int(input("Enter The Number of Rows: "))
# cols = int(input("Enter The Number of Columns: "))
# symbol = input("Enter Your Symbol: ")

# for i in range(rows):
#     for j in range(cols):
#         print(symbol, end="")
#     print()

#SHOPPING CART PROGRAM

# foods = []
# prices = []
# total = 0

# while True:
#     food = input("Enter the food would you like to buy? (press q to quit): ")
#     if food.lower() == "q":
#         break
#     else:
#         price = float(input("Enter The Price of Foods: "))
#         prices.append(price)
#         foods.append(food)

# print("<------ Your Cart ------->")

# for food in foods: 
#     print(food, end = " ")

# for price in prices:
#     total += price
    
# print()
# print(f"Your Total is ${total}")

# PYTHON QUIZ GAME

# questions = ("What is the Square of 2?",
#             "What is square root of 4?")
# options = (("A. 4", "B. 2", "C. 8", "D. 12"),
#             ("A. 4", "B. 2", "C. 8", "D. 10"))

# answers = ("A", "B")
# guesses = []
# score = 0
# question_num = 0

# for question in questions:
#     print("<--------------------------->")
#     print(question)
#     for option in options[question_num]:
#         print(option)

#     guess = input("Enter Your Guess: ").upper()
#     guesses.append(guess)
#     if guesses == answers[question_num]:
#         score += 1
#         print("Correct")
#     else:
#         print("Incorrect")
#         print(f"{answers[question_num]} is the correct answer")

#     question_num += 1

# NUMBER GUESSING GAME

# import random 

# lowest_num = 1
# highest_num = 100
# answer = random.randint(lowest_num, highest_num)
# guesses = 0
# is_running = True

# print("<--------- WELCOME TO PYTHON NUMBER GUESSING GAME ------------>")
# print(f"Guess a Number between {lowest_num} and {highest_num}")

# while is_running:
#     guess = input("Enter your guess: ")
#     if guess.isdigit():
#         guess = int(guess)
#         guesses += 1

#         if guess < lowest_num or guess > highest_num:
#             print("That Number Out Of Range.....")
#             print(f"Please Select a Number between {lowest_num} and {highest_num}")
#         elif guess < answer:
#             print("Too Low! Try again")
#         elif guess > answer:
#             print("Too High! Try Again")
#         else: 
#             print(f"CORRECT! The answer was {answer}")
#             print(f"Number Of Guesses {guesses}")
#             is_running = False

#     else:
#         print("Invalid Guess")
#         print(f"Please Select a Number between {lowest_num} and {highest_num}")

# ROCK/PAPER/SCISSOR GUESSING GAME

# import random

# option = ("rock" , "paper" , "scissor")
# running = True

# while running:
#     player = None
#     computer = random.choice(option)

#     print("<--------- WELCOME TO PYTHON ROCK/PAPER/SCISSOR GUESSING GAME ------------>")

#     while player not in option:
#         player = input("Enter a Choice (rock, paper, choice): ").lower()

#     if player == computer:
#         print("Game is Tie!")
#     elif player == "rock" and computer == "scissor":
#         print("You Win!")    
#     elif player == "paper" and computer == "rock":
#         print("You Win!")
#     elif player == "scissor" and computer == "paper":
#         print("You Win!")
#     else:
#         print("You Lose!")
    
#     if not input("Play Again? (y/n): ").lower() == "y":
#         running = False  
 
# print("Thanks For Playing!")

# BANKING PROGRAM

# balance = 0
# isrunning = True

# def showbal ():
#     print(f"Your Balnce is ${balance:.2f}")

# def deposit ():
#     amount = float(input("Enter An AMount you want to deposit: "))

#     if amount < 0:
#         print("That's not Valid Amout!")
#         return 0
#     else:
#         return amount

# def withdraw ():
#     amount = float(input("Enter an amount you want to withdraw: "))

#     if amount < 0:
#         print("That's Invalid!")
#     elif amount > balance:
#         print("That's InValid!")
#     else:
#         return amount

# while isrunning:
#     print("XYZ BANK POSRTAL")
#     print("================")
#     print("1. Show Balance")
#     print("2. Withdraw")
#     print("3. Deposit")
#     print("4. Exit")

#     choice = input("Enter your choice (1-4): ")

#     if choice == "1":
#         showbal()
#     elif choice == "2":
#         balance -= withdraw()
#     elif choice == "3":
#         balance += deposit()
#     elif choice == "4":
#         isrunning = False
#     else:
#         print("This is not a Valid choice!")