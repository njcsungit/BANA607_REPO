'''
Author: Noel Jiwanmall
'''
class calculator:
    def self(arg_action,arg_x,arg_y):
        action=arg_action
        x=arg_x
        y=arg_y
    
    def add(self,x,y):
        return x*y;

    def multiply(self,x,y):
        return x*y;

    def findaction(self,arg_action):
        match arg_action:
            case 'add':
                return 'add'
            case 'multiply':
                return 'multiply'
            case _:
                return "unknown"


# Using the special variable 
# __name__
if __name__=="__main__":
    input_action=(input("would you like to add or multiply two numbers?: "))
    
    calc=calculator()

    validated_action=calc.findaction(input_action)

    if validated_action!="unknown":
        print("Great! I will help you "+input_action+" two numbers.")
    else:
        print("I am sorry. I cannot perform the action you have entered :(")
        exit()
    
    x=int(input("enter x: "))
    y=int(input("enter y: "))

    
    if validated_action=='add':
        print(str(x)+" + "+str(y)+ " = ",calc.add(x,y))
    else:
        print(str(x)+" x "+str(y)+ " = ",calc.multiply(x,y))

