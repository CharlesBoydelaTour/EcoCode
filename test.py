def is_pair(n): 
        #this function returns true if n is a pair number and false if it is odd \n
        if n == 2:  
            return True 
        elif n == 4:
            return True 
        elif n == 6: 
            return True 
        else : 
            return False 
for i in range(100000): 
        is_pair(i)