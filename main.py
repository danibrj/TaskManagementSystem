
while True:
    order = input(">> ").strip().split()
    
    command = order[0]
    
    if command == "InsertTask":
        t_id = int(order[1])
        startTime = int(order[2])
        endTime = int(order[3])
        value = int(order[4])
        
    elif command == "DeleteTask":
        t_id = int(order[1])

    elif command == "UpdateTask":
        t_id = int(order[1])
        startTime = int(order[2])
        endTime = int(order[3])
        value = int(order[4])
        
    elif command == "QueryTaskId":
        t_id = int(order[1])
        
    elif command == "QueryTaskSum":
        t_id1= int(order[1])
        t_id2 = int(order[2])
        
    elif command == "PrintTrees":
        pass        
    elif command == "exit":
        break
    