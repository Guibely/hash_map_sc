# Name:Guibely De aguinaga
# OSU Email:deaguing@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment:6
# Due Date:12/07/2023
# Description: implement methods for hash map separate chaining


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution

        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output

        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Method updates the key/value pair in the hash map. If the given key already exists in
        the hash map, its associated value must be replaced with the new value.
        """
        # checks if it needs to be resized
        if self.table_load() >= 1:
            self.resize_table(self._capacity * 2)

        # gets correct bucket
        index = self._buckets.get_at_index(self.find_spot(key))

        # checks if bucket already has the key
        if index.contains(key):
            index.remove(key)
            self._size -= 1
            index.insert(key, value)
        else:
            index.insert(key, value)
        self._size += 1

        return

    def find_spot(self, key):
        """ method finds correct index"""

        return self._hash_function(key) % self._capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        Method changes the capacity of the internal hash table. All existing key/value pairs
        must remain in the new hash map, and all hash table links must be rehashed.
        """
        if new_capacity < 1:
            return

        new_arr = DynamicArray()
        # checks that new capacity is a prime number
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)
        self._capacity = new_capacity

        temp_arr = self._buckets
        self._buckets = new_arr
        self._size = 0

        # adds linked list to buckets
        for i in range(self._capacity):
            self._buckets.append(LinkedList())
        # adds keys to nodes
        for node in range(temp_arr.length()):
            for keys in temp_arr.get_at_index(node):
                self.put(keys.key, keys.value)

    def table_load(self) -> float:
        """
        Method returns the current hash table load factor.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        This method returns the number of empty buckets in the hash table
        """
        count = 0
        for i in range(self._buckets.length()):
            val = self._buckets.get_at_index(i)
            if val.length() == 0:
                count += 1
        return count

    def get(self, key: str):
        """
        Method returns the value associated with the given key. If the key is not in
        the hash map, the method returns None.
        """
        if self.contains_key(key) is True:
            val = self._buckets.get_at_index(self.find_spot(key))
            return val.contains(key).value

        return None

    def contains_key(self, key: str) -> bool:
        """
        Method returns True if the given key is in the hash map, otherwise it returns False
        """
        index = self._buckets.get_at_index(self.find_spot(key))
        if index.contains(key):
            return True
        return False

    def remove(self, key: str) -> None:
        """
        Method removes the given key and its associated value from the hash map
        """
        index = self._buckets.get_at_index(self.find_spot(key))
        if index.contains(key):
            index.remove(key)
            self._size -= 1
        return

    def get_keys_and_values(self) -> DynamicArray:
        """
        Method returns a dynamic array where each index contains a tuple of a key/value pair
        stored in the hash map
        """
        arr = DynamicArray()
        for i in range(self._buckets.length()):
            # appends keys and values to array
            for index in self._buckets.get_at_index(i):
                arr.append((index.key, index.value))

        return arr

    def clear(self) -> None:
        """
        Method clears the contents of the hash map. It does not change the underlying hash
        table capacity
        """
        for i in range(self._capacity):
            index = self._buckets.get_at_index(i)
            # remove nodes in linked list
            for node in index:
                if index.contains(node.key):
                    index.remove(node.key)
                    self._size -= 1


def find_mode(da: DynamicArray) -> tuple:
    """
    This function will return a tuple containing, in this
    order, a dynamic array comprising the mode (most occurring) value(s) of the given array,
    and an integer representing the highest frequency of occurrence for the mode value(s).
    """
    map = HashMap()
    # loop through array
    # add key and value to map, value being the frequency
    for i in range(da.length()):
        index_val = da.get_at_index(i)
        if not map.contains_key(index_val):
            map.put(index_val, 1)
        else:
            map.put(index_val, map.get(index_val) + 1)

    # dynamic array for map's mode
    arr_mode = DynamicArray()
    arr = map.get_keys_and_values()

    frequency = 0
    # check which value is the highest
    for i in range(arr.length()):
        index_val = arr.get_at_index(i)
        if frequency < index_val[1]:
            frequency = index_val[1]

    # loop through array to check if value equals frequency
    for i in range(arr.length()):
        index_val = arr.get_at_index(i)
        if index_val[1] == frequency:
            arr_mode.append(index_val[0])

    return arr_mode, frequency


# ------------------- BASIC TESTING ---------------------------------------- #
#
# if __name__ == "__main__":
# #
    # print("\nPDF - put example 1")
    # print("-------------------")
    # m = HashMap(53, hash_function_1)
    # # t = HashMap(7, )
    # for i in range(150):
    #     m.put('str' + str(i), i * 100)
    #     if i % 25 == 24:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    # print("\nPDF - put example 2")
    # print("-------------------")
    # m = HashMap(41, hash_function_2)
    # for i in range(50):
    #     m.put('str' + str(i // 3), i * 100)
    #     if i % 10 == 9:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - resize example 1")
    # print("----------------------")
    # m = HashMap(20, hash_function_1)
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    # m.resize_table(30)
    # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    #
    # print("\nPDF - resize example 2")
    # print("----------------------")
    # m = HashMap(75, hash_function_2)
    # keys = [i for i in range(1, 1000, 13)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())
    #
    # for capacity in range(111, 1000, 117):
    #     m.resize_table(capacity)
    #
    #     m.put('some key', 'some value')
    #     result = m.contains_key('some key')
    #     m.remove('some key')
    #
    #     for key in keys:
    #         # all inserted keys must be present
    #         result &= m.contains_key(str(key))
    #         # NOT inserted keys must be absent
    #         result &= not m.contains_key(str(key + 1))
    #     print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    # print("\nPDF - table_load example 1")
    # print("--------------------------")
    # m = HashMap(101, hash_function_1)
    # print(round(m.table_load(), 2))
    # m.put('key1', 10)
    # print(round(m.table_load(), 2))
    # m.put('key2', 20)
    # print(round(m.table_load(), 2))
    # m.put('key1', 30)
    # print(round(m.table_load(), 2))
    #
    # print("\nPDF - table_load example 2")
    # print("--------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(50):
    #     m.put('key' + str(i), i * 100)
    #     if i % 10 == 0:
    #         print(round(m.table_load(), 2), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - empty_buckets example 1")
    # print("-----------------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 30)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key4', 40)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - empty_buckets example 2")
    # print("-----------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('key' + str(i), i * 100)
    #     if i % 30 == 0:
    #         print(m.empty_buckets(), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - get example 1")
    # print("-------------------")
    # m = HashMap(31, hash_function_1)
    # print(m.get('key'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    #
    # print("\nPDF - get example 2")
    # print("-------------------")
    # m = HashMap(151, hash_function_2)
    # for i in range(200, 300, 7):
    #     m.put(str(i), i * 10)
    # print(m.get_size(), m.get_capacity())
    # for i in range(200, 300, 21):
    #     print(i, m.get(str(i)), m.get(str(i)) == i * 10)
    #     print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    # print("\nPDF - contains_key example 1")
    # print("----------------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.contains_key('key1'))
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key3', 30)
    # print(m.contains_key('key1'))
    # print(m.contains_key('key4'))
    # print(m.contains_key('key2'))
    # print(m.contains_key('key3'))
    # m.remove('key3')
    # print(m.contains_key('key3'))
    #
    # print("\nPDF - contains_key example 2")
    # print("----------------------------")
    # m = HashMap(79, hash_function_2)
    # keys = [i for i in range(1, 1000, 20)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())
    # result = True
    # for key in keys:
    #     # all inserted keys must be present
    #     result &= m.contains_key(str(key))
    #     # NOT inserted keys must be absent
    #     result &= not m.contains_key(str(key + 1))
    # print(result)
    #
    # print("\nPDF - remove example 1")
    # print("----------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get('key1'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    # m.remove('key1')
    # print(m.get('key1'))
    # m.remove('key4')
    #
    # print("\nPDF - get_keys_and_values example 1")
    # print("------------------------")
    # m = HashMap(11, hash_function_2)
    # for i in range(1, 6):
    #     m.put(str(i), str(i * 10))
    # print(m.get_keys_and_values())
    #
    # m.put('20', '200')
    # m.remove('1')
    # m.resize_table(2)
    # print(m.get_keys_and_values())
    #
    # print("\nPDF - clear example 1")
    # print("---------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key1', 30)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())
    #
    # print("\nPDF - clear example 2")
    # print("---------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.get_size(), m.get_capacity())
    # m.resize_table(100)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())
    #
    # print("\nPDF - find_mode example 1")
    # print("-----------------------------")
    # da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    # mode, frequency = find_mode(da)
    # print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")
    #
    # print("\nPDF - find_mode example 2")
    # print("-----------------------------")
    # test_cases = (
    #     ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
    #     ["one", "two", "three", "four", "five"],
    #     ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    # )
    #
    # for case in test_cases:
    #     da = DynamicArray(case)
    #     mode, frequency = find_mode(da)
    #     print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
