class SegmentTree:
    def __init__(self, max_id):
        self.n = max_id
        self.tree = [0] * (4 * self.n)
        self._build(1, 1, self.n)

    # =========================
    # Build اولیه (درخت خالی)
    # =========================
    def _build(self, node, start, end):
        if start == end:
            self.tree[node] = 0
            return

        mid = (start + end) // 2
        self._build(node * 2, start, mid)
        self._build(node * 2 + 1, mid + 1, end)
        self.tree[node] = 0

    # =========================
    # API عمومی (مطابق پروژه)
    # =========================

    def insert_task(self, task_id, value):
        self._update(1, 1, self.n, task_id, value)

    def update_task(self, task_id, value):
        self._update(1, 1, self.n, task_id, value)

    def delete_task(self, task_id):
        self._update(1, 1, self.n, task_id, 0)

    def query_task_sum(self, id1, id2):
        if id1 > id2:
            id1, id2 = id2, id1
        return self._query(1, 1, self.n, id1, id2)

    # =========================
    # توابع داخلی الگوریتمی
    # =========================

    def _update(self, node, start, end, idx, value):
        if start == end:
            self.tree[node] = value
            return

        mid = (start + end) // 2
        if idx <= mid:
            self._update(node * 2, start, mid, idx, value)
        else:
            self._update(node * 2 + 1, mid + 1, end, idx, value)

        self.tree[node] = self.tree[node * 2] + self.tree[node * 2 + 1]

    def _query(self, node, start, end, l, r):
        if r < start or end < l:
            return 0

        if l <= start and end <= r:
            return self.tree[node]

        mid = (start + end) // 2
        return (
            self._query(node * 2, start, mid, l, r) +
            self._query(node * 2 + 1, mid + 1, end, l, r)
        )

    # =========================
    # چاپ درخت (برای PrintTrees)
    # =========================
    def print_tree(self):
        self._print_tree(1, 1, self.n, 0)

    def _print_tree(self, node, start, end, level):
        if start > end or self.tree[node] == 0:
            return

        print("  " * level + f"[{start}, {end}] -> sum = {self.tree[node]}")
        if start != end:
            mid = (start + end) // 2
            self._print_tree(node * 2, start, mid, level + 1)
            self._print_tree(node * 2 + 1, mid + 1, end, level + 1)


# x = SegmentTree(10000)
# x.insert_task(1,40)
# x.insert_task(2,10)
# x.insert_task(3,30)
# x.insert_task(4,20)
# x.insert_task(5,5)
# x.insert_task(6,15)
# print(x.query_task_sum(1,6))
# x.print_tree()


