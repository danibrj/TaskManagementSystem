# تعریف Node بیرون از کلاس درخت
class Node:
    def __init__(self, task_id, start, end, value):
        self.task_id = task_id
        self.start = start
        self.end = end
        self.value = value
        self.max_end = end
        self.left = None
        self.right = None


class IntervalTree:
    def __init__(self):
        self.root = None

    # بررسی تداخل دو بازه
    def _is_overlap(self, s1, e1, s2, e2):
        return s1 < e2 and s2 < e1

    # جستجوی همه تداخل‌ها
    def _search_conflicts(self, node, start, end, result):
        if node is None:
            return
        if self._is_overlap(start, end, node.start, node.end):
            result.append(node)
        if node.left and node.left.max_end >= start:
            self._search_conflicts(node.left, start, end, result)
        self._search_conflicts(node.right, start, end, result)

    # اضافه کردن تسک با چک تداخل
    def insert_task(self, task_id, start, end, value):
        conflicts = []
        self._search_conflicts(self.root, start, end, conflicts)
        if conflicts:
            for node in conflicts:
                print(f"there is a conflict between {task_id} and {node.task_id}")
            return False
        self.root = self._insert(self.root, task_id, start, end, value)
        return True

    # Insert داخلی (BST بر اساس start)
    def _insert(self, node, task_id, start, end, value):
        if node is None:
            return Node(task_id, start, end, value)
        if start < node.start:
            node.left = self._insert(node.left, task_id, start, end, value)
        else:
            node.right = self._insert(node.right, task_id, start, end, value)
        node.max_end = max(node.max_end, end)
        return node

    # پیدا کردن مینیمم نود (برای Delete)
    def _min_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    # حذف تسک
    def delete_task(self, task_id):
        self.root = self._delete(self.root, task_id)

    def _delete(self, node, task_id):
        if node is None:
            return None
        if task_id < node.task_id:
            node.left = self._delete(node.left, task_id)
        elif task_id > node.task_id:
            node.right = self._delete(node.right, task_id)
        else:
            # نود پیدا شد
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            successor = self._min_node(node.right)
            node.task_id = successor.task_id
            node.start = successor.start
            node.end = successor.end
            node.value = successor.value
            node.right = self._delete(node.right, successor.task_id)

        node.max_end = node.end
        if node.left:
            node.max_end = max(node.max_end, node.left.max_end)
        if node.right:
            node.max_end = max(node.max_end, node.right.max_end)

        return node

    # آپدیت تسک
    def update_task(self, task_id, start, end, value):
        self.delete_task(task_id)
        return self.insert_task(task_id, start, end, value)

    # چاپ درخت
    def print_tree(self):
        self._print(self.root, 0)

    def _print(self, node, level):
        if node is None:
            return
        self._print(node.right, level + 1)
        print("    " * level +
              f"[ID:{node.task_id} "
              f"({node.start},{node.end}) "
              f"maxEnd={node.max_end}]")
        self._print(node.left, level + 1)



x = IntervalTree()
x.insert_task(1,10,15,50)
x.insert_task(2,16,20,50)
x.insert_task(3,21,25,50)
x.insert_task(4,26,30,50)

x.insert_task(5,18,34,67)
x.print_tree()
