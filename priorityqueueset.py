import heapq

class Priorities():
    def __init__(self):
        self.set = {}
        self.heap = []

    def __len__(self):
        return len(self.heap)

    def item_exists(self, item): # Checks whether the item exists in the queue
        return item in self.set

    def pop_smallest(self):
        smallest = heapq.heappop(self.heap)
        del self.set[smallest]
        return smallest

    def add(self, item):
        # This adds the item to the queue.

        if not item in self.set:
            self.set[item] = item
            heapq.heappush(self.heap, item)
            return True
        elif item < self.set[item]:
            for x, old_items in enumerate(self.heap):
                if old_items == item:
                    del self.heap[x]
                    self.heap.append(item)
                    heapq.heapify(self.heap)
                    self.set[item] = item
                    return True

        return False

if __name__ == "__main__":
    import unittest # Probably the most suited library.

    # assertEqual checks for an expected result.
    #
    class TestPriorities(unittest.TestCase):
        def test_int(self):
            priority = Priority()
            for x in [3, 5, 2, 2, 99, 23]:
                priority.add(x)

            self.assert_(priority.item_exists(3))
            self.assert_(priority.item_exists(2))
            self.assert_(priority.item_exists(99))
            self.assert_(not priority.item_exists(4))
            self.assertEqual(len(priority), 5)

            self.assertEqual(priority.pop_smallest(), 2)
            self.assertEqual(priority.pop_smallest(), 3)
            self.assertEqual(len(priority), 3)

            priority.add(1)
            self.assertEqual(len(priority), 4)
            self.assertEqual(priority.pop_smallest(), 1)
            self.assertEqual(priority.pop_smallest(), 5)
            self.assertEqual(priority.pop_smallest(), 23)
            self.assertEqual(priority.pop_smallest(), 99)
            self.assertRaises(IndexError, priority.pop_smallest)
            self.assertEqual(len(priority), 0)

            self.assert_(priority.add(6))
            self.assert_(priority.add(16))
            self.assert_(priority.add(2))
            self.assertEqual(priority.pop_smallest(), 2)
            self.assert_(not priority.add(6))
            self.assert_(not priority.add(16))
            self.assert_(priority.add(2))
            self.assertEqual(priority.pop_smallest(), 2)
            self.assertEqual(priority.pop_smallest(), 6)
            self.assertEqual(priority.pop_smallest(), 16)
            self.assertRaises(IndexError, priority.pop_smallest)
