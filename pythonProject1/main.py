
# C950 - Webinar-2 - Getting Greedy, who moved my data?
# W-2_ChainingHashTable_zyBooks_Key-Value_CSV_Greedy.py
# Ref: zyBooks: Figure 7.8.2: Hash table using chaining.
# Ref: zyBooks: 3.3.1: MakeChange greedy algorithm.


import csv
import math


# HashTable class using chaining.
class ChainingHashTable:
    # Constructor with optional initial capacity parameter.
    # Assigns all buckets with an empty list.
    def __init__(self, initial_capacity=10):
        # initialize the hash table with empty bucket list entries.
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Inserts a new item into the hash table.
    def insert(self, key, item):  # does both insert and update
        # get the bucket list where this item will go.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # update key if it is already in the bucket
        for kv in bucket_list:
            # print (key_value)
            if kv[0] == key:
                kv[1] = item
                return True

        # if not, insert the item to the end of the bucket list.
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # Searches for an item with matching key in the hash table.
    # Returns the item if found, or None if not found.
    def search(self, key):
        # get the bucket list where this key would be.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        # print(bucket_list)

        # search for the key in the bucket list
        for kv in bucket_list:
            # print (key_value)
            if kv[0] == key:
                return kv[1]  # value
        return None

    # Removes an item with matching key from the hash table.
    def remove(self, key):
        # get the bucket list where this item will be removed from.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # remove the item from the bucket list if it is present.
        for kv in bucket_list:
            # print (key_value)
            if kv[0] == key:
                bucket_list.remove([kv[0], kv[1]])


class Package:
    def __init__(self, packageID, address, city, state, zipcode, deliveryDeadline, weight, note):
        self.packageID = packageID
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deliveryDeadline = deliveryDeadline
        self.weight = weight
        self.note = note

    def __str__(self):  # overwite print(Package) otherwise it will print object reference
        return "%s, %s, %s, %s, %s, %s, %s, %s" % (self.packageID, self.address, self.city, self.state, self.zipcode,
                                                   self.deliveryDeadline, self.weight, self.note)


def loadPackageData(fileName):
    with open(fileName) as packages:
        packageData = csv.reader(packages, delimiter=',')
        next(packageData)  # skip header
        for package in packageData:
            packageID = package[0]
            address = package[1]
            city = package[2]
            state = package[3]
            zipcode = package[4]
            deliveryDeadline = package[5]
            weight = package[6]
            note = package[7]

            # package object
            p = Package(packageID, address, city, state, zipcode, deliveryDeadline, weight, note)
            # print(p)

            # insert it into the hash table
            packageHash.insert(packageID, p)


# Hash table instance
packageHash = ChainingHashTable()
loadPackageData('packages.csv')

# Fetch data from Hash Table
for i in range(len(packageHash.table)+1):
    print("Movie: {}".format(packageHash.search(i+1)))  # 1 to 11 is sent to myHash.search()
