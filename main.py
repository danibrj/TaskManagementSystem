from mangeTasks import ManageTasks

mT = ManageTasks()

while True:
    order = input(">> ").strip().split()
    
    command = order[0]
    
    if command == "InsertTask":
        t_id = int(order[1])
        startTime = int(order[2])
        endTime = int(order[3])
        value = int(order[4])
        mT.insertTask(t_id,startTime,endTime,value)
        
    elif command == "DeleteTask":
        t_id = int(order[1])
        mT.deleteTask(t_id)

    elif command == "UpdateTask":
        t_id = int(order[1])
        startTime = int(order[2])
        endTime = int(order[3])
        value = int(order[4])
        mT.updateTask(t_id,startTime,endTime,value)
        
    elif command == "QueryTaskId":
        t_id = int(order[1])
        mT.queryTaskId(t_id)
        
    elif command == "QueryTaskSum":
        t_id1= int(order[1])
        t_id2 = int(order[2])
        mT.queryTaskSum(t_id1,t_id2)
        
    elif command == "PrintTrees":
        mT.printTrees()
        
    elif command == "exit":
        break
    