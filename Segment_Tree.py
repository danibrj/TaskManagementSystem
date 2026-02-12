# class SegmentTree:
#     def __init__(self, max_id):
#         self.n = max_id
#         self.tree = [0] * (4 * self.n)
#         self._build(1, 1, self.n)

#     # =========================
#     # Build اولیه (درخت خالی)
#     # =========================
#     def _build(self, node, start, end):
#         if start == end:
#             self.tree[node] = 0
#             return

#         mid = (start + end) // 2
#         self._build(node * 2, start, mid)
#         self._build(node * 2 + 1, mid + 1, end)
#         self.tree[node] = 0

#     # =========================
#     # API عمومی (مطابق پروژه)
#     # =========================

#     def insert_task(self, task_id, value):
#         self._update(1, 1, self.n, task_id, value)

#     def update_task(self, task_id, value):
#         self._update(1, 1, self.n, task_id, value)

#     def delete_task(self, task_id):
#         self._update(1, 1, self.n, task_id, 0)

#     def query_task_sum(self, id1, id2):
#         if id1 > id2:
#             id1, id2 = id2, id1
#         return self._query(1, 1, self.n, id1, id2)

#     # =========================
#     # توابع داخلی الگوریتمی
#     # =========================

#     def _update(self, node, start, end, idx, value):
#         if start == end:
#             self.tree[node] = value
#             return

#         mid = (start + end) // 2
#         if idx <= mid:
#             self._update(node * 2, start, mid, idx, value)
#         else:
#             self._update(node * 2 + 1, mid + 1, end, idx, value)

#         self.tree[node] = self.tree[node * 2] + self.tree[node * 2 + 1]

#     def _query(self, node, start, end, l, r):
#         if r < start or end < l:
#             return 0

#         if l <= start and end <= r:
#             return self.tree[node]

#         mid = (start + end) // 2
#         return (
#             self._query(node * 2, start, mid, l, r) +
#             self._query(node * 2 + 1, mid + 1, end, l, r)
#         )

#     # =========================
#     # چاپ درخت (برای PrintTrees)
#     # =========================
#     def print_tree(self):
#         self._print_tree(1, 1, self.n, 0)

#     def _print_tree(self, node, start, end, level):
#         if start > end or self.tree[node] == 0:
#             return

#         print("  " * level + f"[{start}, {end}] -> sum = {self.tree[node]}")
#         if start != end:
#             mid = (start + end) // 2
#             self._print_tree(node * 2, start, mid, level + 1)
#             self._print_tree(node * 2 + 1, mid + 1, end, level + 1)
class Node:
    def __init__(self):
        self.sum = 0
        self.left = None
        self.right = None


class SegmentTree:
    def __init__(self):
        self.root = None
        self.max_id = 0
        self.data = {}  # نگه‌داری مقادیر واقعی (id -> value)

    def insert_task(self, task_id, value):
        self.data[task_id] = value
        if task_id > self.max_id:
            self._rebuild(task_id)
        else:
            self._update(self.root, 1, self.max_id, task_id, value)

    def update_task(self, task_id, value):
        self.insert_task(task_id, value)

    def delete_task(self, task_id):
        if task_id in self.data:
            self.data[task_id] = 0
            self._update(self.root, 1, self.max_id, task_id, 0)

    def query_task_sum(self, l, r):
        if self.root is None:
            return 0
        l = max(1, l)
        r = min(self.max_id, r)
        if l > r:
            return 0
        return self._query(self.root, 1, self.max_id, l, r)

    # ======================
    # بازسازی کامل درخت
    # ======================
    def _rebuild(self, new_max):
        self.max_id = new_max
        self.root = Node()
        for idx, val in self.data.items():
            if val != 0:
                self._update(self.root, 1, self.max_id, idx, val)

    # ======================
    # توابع داخلی
    # ======================
    def _update(self, node, start, end, idx, value):
        if start == end:
            node.sum = value
            return

        mid = (start + end) // 2
        if idx <= mid:
            if node.left is None:
                node.left = Node()
            self._update(node.left, start, mid, idx, value)
        else:
            if node.right is None:
                node.right = Node()
            self._update(node.right, mid + 1, end, idx, value)

        node.sum = (node.left.sum if node.left else 0) + \
                   (node.right.sum if node.right else 0)

    def _query(self, node, start, end, l, r):
        if node is None or r < start or end < l:
            return 0
        if l <= start and end <= r:
            return node.sum

        mid = (start + end) // 2
        return self._query(node.left, start, mid, l, r) + \
               self._query(node.right, mid + 1, end, l, r)
               
    def print_tree(self):
        if self.root is None:
            print("Tree is empty")
            return
        print(f"Max ID: {self.max_id}")
        self._print_tree(self.root, 1, self.max_id, 0)


    def _print_tree(self, node, start, end, level):
        if node is None or node.sum == 0:
            return

        print("  " * level + f"[{start}, {end}] -> sum = {node.sum}")

        if start == end:
            return

        mid = (start + end) // 2
        self._print_tree(node.left, start, mid, level + 1)
        self._print_tree(node.right, mid + 1, end, level + 1)



# # تست
# x = SegmentTree()
# x.insert_task(1,40)
# x.insert_task(2,10)
# x.insert_task(3,30)
# x.insert_task(4,20)
# x.insert_task(5,5)
# x.insert_task(6,15)
# print(x.query_task_sum(2,6))  
# x.print_tree()

# x.delete_task(3)
# print(x.query_task_sum(2,6))  

# x.print_tree()


