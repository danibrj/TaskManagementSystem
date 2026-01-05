class Task:
    def __init__(self,t_id,start_time,end_time,value):
        self.t_id = t_id
        self.start_time = start_time
        self.end_time = end_time
        self.value = value
    
    def __str__(self):
        return f"Task => id:{self.t_id} |start time: {self.start_time} |end time: {self.end_time} |value: {self.value}"

    def __repr__(self):
        return self.__str__()


# x = Task(1,10,15,50)
# print(x)