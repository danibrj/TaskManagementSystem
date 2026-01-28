from Task import Task

class BTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t
        self.leaf = leaf
        self.keys = []      # ذخیره Task ها
        self.children = []


class BTree:
    def __init__(self, t):
        self.t = t
        self.root = BTreeNode(t, leaf=True)

    # ===== جست‌وجو بر اساس Task.id =====
    def search(self, task_id):
        return self._search(self.root, task_id)
    
    def search_for_update(self,task_id,startTime,endTime,value):
        task = self._search(self.root, task_id)
        if task:
            task.start_time = startTime
            task.end_time = endTime
            task.value = value
            return True
        return False

    def _search(self, node, task_id):
        i = 0
        while i < len(node.keys) and task_id > node.keys[i].t_id:
            i += 1

        if i < len(node.keys) and node.keys[i].t_id == task_id:
            return node.keys[i]

        if node.leaf:
            return None

        return self._search(node.children[i], task_id)


    
    # ===== درج =====
    def insert(self, task):
        root = self.root
        if len(root.keys) == 2 * self.t - 1:
            new_root = BTreeNode(self.t, leaf=False)
            new_root.children.append(root)
            self._split_child(new_root, 0)
            self.root = new_root
            self._insert_non_full(new_root, task)
        else:
            self._insert_non_full(root, task)

    def _insert_non_full(self, node, task):
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append(None)
            while i >= 0 and task.t_id < node.keys[i].t_id:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = task
        else:
            while i >= 0 and task.t_id < node.keys[i].t_id:
                i -= 1
            i += 1
            if len(node.children[i].keys) == 2 * self.t - 1:
                self._split_child(node, i)
                if task.t_id > node.keys[i].t_id:
                    i += 1
            self._insert_non_full(node.children[i], task)

    def _split_child(self, parent, index):
        t = self.t
        full_child = parent.children[index]
        new_child = BTreeNode(t, leaf=full_child.leaf)
        parent.keys.insert(index, full_child.keys[t - 1])
        parent.children.insert(index + 1, new_child)

        new_child.keys = full_child.keys[t:]
        full_child.keys = full_child.keys[:t - 1]

        if not full_child.leaf:
            new_child.children = full_child.children[t:]
            full_child.children = full_child.children[:t]

    # ===== حذف =====
    def delete(self, task_id):
        self._delete(self.root, task_id)
        # اگر ریشه خالی شد، فرزند اول را به ریشه جدید تبدیل کن
        if len(self.root.keys) == 0 and not self.root.leaf:
            self.root = self.root.children[0]

    def _delete(self, node, task_id):
        t = self.t
        i = 0
        while i < len(node.keys) and task_id > node.keys[i].t_id:
            i += 1

        # حالت 1: کلید در نود فعلی یافت شد
        if i < len(node.keys) and node.keys[i].t_id == task_id:
            if node.leaf:
                # ساده‌ترین حالت: فقط حذف
                node.keys.pop(i)
            else:
                # حذف از نود داخلی
                left_child = node.children[i]
                right_child = node.children[i + 1]

                # اگر فرزند چپ حداقل t کلید دارد
                if len(left_child.keys) >= t:
                    pred = self._get_predecessor(left_child)
                    node.keys[i] = pred
                    self._delete(left_child, pred.t_id)
                # اگر فرزند راست حداقل t کلید دارد
                elif len(right_child.keys) >= t:
                    succ = self._get_successor(right_child)
                    node.keys[i] = succ
                    self._delete(right_child, succ.t_id)
                else:
                    # merge و حذف کلید
                    self._merge(node, i)
                    self._delete(left_child, task_id)
            return

        # حالت 2: کلید در نود فعلی نیست
        if node.leaf:
            return  # کلید وجود ندارد

        # قبل از حرکت به فرزند، اطمینان از حداقل t کلید
        child = node.children[i]
        if len(child.keys) < t:
            if i > 0 and len(node.children[i - 1].keys) >= t:
                self._borrow_from_prev(node, i)
            elif i < len(node.children) - 1 and len(node.children[i + 1].keys) >= t:
                self._borrow_from_next(node, i)
            else:
                if i < len(node.children) - 1:
                    self._merge(node, i)
                    child = node.children[i]
                else:
                    self._merge(node, i - 1)
                    child = node.children[i - 1]

        self._delete(child, task_id)

    # ===== عملیات کمکی برای حذف =====
    def _get_predecessor(self, node):
        while not node.leaf:
            node = node.children[-1]
        return node.keys[-1]

    def _get_successor(self, node):
        while not node.leaf:
            node = node.children[0]
        return node.keys[0]

    def _merge(self, parent, idx):
        child = parent.children[idx]
        sibling = parent.children[idx + 1]
        t = self.t

        # انتقال کلید والد به child
        child.keys.append(parent.keys[idx])
        # اضافه کردن کلیدها و فرزندان sibling
        child.keys.extend(sibling.keys)
        if not sibling.leaf:
            child.children.extend(sibling.children)
        # حذف کلید و فرزند اضافی
        parent.keys.pop(idx)
        parent.children.pop(idx + 1)

    def _borrow_from_prev(self, parent, idx):
        child = parent.children[idx]
        sibling = parent.children[idx - 1]
        # انتقال کلید از والد و برادر
        child.keys.insert(0, parent.keys[idx - 1])
        parent.keys[idx - 1] = sibling.keys.pop(-1)
        if not sibling.leaf:
            child.children.insert(0, sibling.children.pop(-1))

    def _borrow_from_next(self, parent, idx):
        child = parent.children[idx]
        sibling = parent.children[idx + 1]
        # انتقال کلید از والد و برادر
        child.keys.append(parent.keys[idx])
        parent.keys[idx] = sibling.keys.pop(0)
        if not sibling.leaf:
            child.children.append(sibling.children.pop(0))

    # ===== چاپ درخت =====
    def print_tree(self, node=None, level=0, parent_id=None):
        if node is None:
            node = self.root
            print("B-Tree Structure:")

        pid = f"{parent_id}" if parent_id is not None else "Root"
        print("  " * level + f"[Level {level}] Parent: {pid}, Keys: {[k for k in node.keys]}")

        if not node.leaf:
            for idx, child in enumerate(node.children):
                child_id = f"{node.keys[idx].t_id}" if idx < len(node.keys) else f"{node.keys[-1].t_id}+"
                self.print_tree(child, level + 1, parent_id=child_id)


# x = BTree(2)
# y = Task(1,10,15,50)
# y2 = Task(2,15,20,80)
# y3 = Task(3,20,25,60)
# y4 = Task(4,25,30,550)
# y5 = Task(5,25,30,550)
# y6 = Task(6,25,30,550)
# y7 = Task(3.5,25,30,550)





# x.insert(y)
# x.insert(y2)
# x.insert(y3)
# x.insert(y4)
# x.insert(y5)
# x.insert(y6)
# x.insert(y7)




# x.print_tree()
# x.delete(4)
# x.print_tree()

