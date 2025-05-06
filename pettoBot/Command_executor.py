import time

class Command_executor:
    
    def execute(self, func, *args):
        with open('logs.txt', 'a') as f:
            print(f"***{time.strftime("%Y-%m-%d, %H:%M:%S", time.localtime())} Executing function: {func.__name__}", file=f)
            
            try:
                if (len(args) == 1):
                    results = func(args[0])
                elif (len(args) == 2):
                    results = func(args[0], args[1])
            except:
                print(f"Function exeution failed.\n", file=f)
            else:    
                print(f"Function executed successfully.\n", file=f)
                return results
        