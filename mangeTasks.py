from Task import Task
from B_Tree import BTree
from Segment_Tree import SegmentTree
from IntervalTree import IntervalTree
class ManageTasks:
    def __init__(self):
        self.datas = BTree(2)
        self.seg = SegmentTree(10000)
        self.inter = IntervalTree()
    
    def insertTask(self,t_id,startTime,endTime,value):
        task = Task(t_id,startTime,endTime,value)
        isOk = self.inter.insert_task(t_id,startTime,endTime,value)
        if not isOk:
            return
        self.datas.insert(task)
        self.seg.insert_task(task.t_id,task.value)
    
    def deleteTask(self,t_id):
        self.datas.delete(t_id) 
        self.seg.delete_task(t_id)
        self.inter.delete_task(t_id)
    
    def updateTask(self,t_id,startTime,endTime,value):
        res = self.datas.search_for_update(t_id,startTime,endTime,value)
        if not res:
            print("Not found for update")
            return
        self.seg.update_task(t_id,value)
        self.inter.update_task(t_id,startTime,endTime,value)
    
    def queryTaskId(self,t_id):
        task = self.datas.search(t_id)
        print(task)
    
    def queryTaskSum(self,t_id1,t_id2):
        print(self.seg.query_task_sum(t_id1,t_id2))
    
    def printTrees(self):
        print("B-Tree:")
        self.datas.print_tree()
        print("================================================================")
        print("Segment-Tree:")
        self.seg.print_tree()
        print("================================================================")
        print("Interval Tree:")
        self.inter.print_tree()
    
    

# x = ManageTasks()
# # y = Task(1,10,15,50)
# # y2 = Task(2,15,20,80)
# # y3 = Task(3,20,25,60)
# # y4 = Task(4,25,30,550)
# # y5 = Task(5,25,30,550)
# # y6 = Task(6,25,30,550)
# # y7 = Task(3.5,25,30,550)





# x.insertTask(1,10,15,50)
# x.insertTask(2,10,15,50)
# x.insertTask(3,10,15,50)
# x.insertTask(4,10,15,50)
# x.insertTask(5,10,15,50)
# x.insertTask(6,10,15,50)



# # x.printTrees()
# x.queryTaskId(4)


# # x.printTrees()
# x.queryTaskSum(2,4)

