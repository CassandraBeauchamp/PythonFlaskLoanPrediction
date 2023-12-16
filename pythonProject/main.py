# Made by WGU Student Cassandra Beauchamp ID#: 011631377

import csv
import datetime


class ChainingHashMap:
    def __init__(self):  # initialize the hash table
        self.size = 40
        self.map = [None] * self.size

    def getHash(self, key):
        hashs = 0
        for char in str(key):
            hashs += ord(char)
        return hashs % self.size

    def add(self, key, value):  # Adds a new item into the table
        keyHash = self.getHash(key)
        keyValue = [key, value]

        if self.map[keyHash] is None:
            self.map[keyHash] = list([keyValue])
            return True
        else:  # update key if it already exists
            for pair in self.map[keyHash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            self.map[keyHash].append(keyValue)
            return True

    def get(self, key):  # return the item at the key
        keyHash = self.getHash(key)
        if self.map[keyHash] is not None:
            for pair in self.map[keyHash]:
                if int(pair[0]) == key:
                    return pair[1]
        return None

    def delete(self, key):  # delete an index of the hash map
        keyHash = self.getHash(key)

        if self.map[keyHash] is None:
            return False
        for i in range(0, len(self.map[keyHash])):
            if self.map[keyHash][i][0] == key:
                self.map[keyHash].pop(i)
                return True
        return False


class Package:  # Class for packages
    def __init__(self, packageID, address, city, state, zipcode, deliveryDeadline, weight, note):
        self.packageID = packageID
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deliveryDeadline = deliveryDeadline
        self.left = None
        self.weight = weight
        self.note = note
        self.status = 'at hub'
        self.deliveredTime = datetime.timedelta(hours=int(0), minutes=int(0), seconds=int(0))

    def __str__(self):  # overwite print(Package) otherwise it will print object reference
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.packageID, self.address, self.city, self.state,
                                                               self.zipcode, self.deliveryDeadline, self.left,
                                                               self.weight,
                                                               self.note, self.status, self.deliveredTime)

    def changeStatus(self, time):  # change status of package
        if self.deliveredTime < time:
            self.status = 'Delivered'  # if user time is after the delivered time it's delivered
        elif self.left < time:
            self.status = "On its way"  # if user time is after the time the package left the hub it's on its way


class Truck:  # Class for Trucks
    def __init__(self, packages, address, departTime):
        self.packages = packages
        self.address = address
        self.departTime = departTime
        self.speed = 18
        self.capacity = 16
        self.time = departTime
        self.mileage = 0

    def __str__(self):  # overwite print(Truck) otherwise it will print object reference
        return "%s, %s, %s, %s, %s, %s, %s" % (self.packages, self.address, self.departTime, self.speed, self.capacity,
                                               self.time, self.mileage)

    def updatePackages(self, time): # change the statuses for all packages in the truck
        for package in self.packages:
            packageHash.get(package).changeStatus(time)


def loadPackageData(fileName):  # to load my packages data into package classes
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
            pack = Package(packageID, address, city, state, zipcode, deliveryDeadline, weight, note)

            # insert it into the hash table
            packageHash.add(packageID, pack)


def loadAddressData(fileName, list):  # to load my address data into address list
    with open(fileName) as addresses:
        addressData = csv.reader(addresses, delimiter=',')
        for addresss in addressData:  # get data from the file
            addressID = addresss[0]
            place = addresss[1]
            address = addresss[2]

            col = [address]
            list.append(col)  # add needed address to the list


def loadDistanceData(fileName, list):  # to load my address data into address list
    with open(fileName) as distances:
        distanceData = csv.reader(distances, delimiter=',')
        for distance in distanceData:  # get distances from file
            distance0 = distance[0]
            distance1 = distance[1]
            distance2 = distance[2]
            distance3 = distance[3]
            distance4 = distance[4]
            distance5 = distance[5]
            distance6 = distance[6]
            distance7 = distance[7]
            distance8 = distance[8]
            distance9 = distance[9]
            distance10 = distance[10]
            distance11 = distance[11]
            distance12 = distance[12]
            distance13 = distance[13]
            distance14 = distance[14]
            distance15 = distance[15]
            distance16 = distance[16]
            distance17 = distance[17]
            distance18 = distance[18]
            distance19 = distance[19]
            distance20 = distance[20]
            distance21 = distance[21]
            distance22 = distance[22]
            distance23 = distance[23]
            distance24 = distance[24]
            distance25 = distance[25]
            distance26 = distance[26]

            col = [distance0, distance1, distance2, distance3, distance4, distance5, distance6, distance7, distance8,
                   distance9, distance10, distance11, distance12, distance13, distance14, distance15, distance16,
                   distance17, distance18, distance19, distance20, distance21, distance22, distance23, distance24,
                   distance25, distance26]  # make a new colum with all the distances
            list.append(col)  # add colum to list


def getDistance(x, y):  # get distance method
    distances = distance[x][y]  # get the coordinates from distance list
    if distances == '':  # inverse coordinates if needed
        distances = distance[y][x]

    return float(distances)


def sendTruck(truck):  # Send a truck out to delivery the packages
    delivering = []  # list of packages to be delivered
    for package in truck.packages:  # adding packages to list
        delivering.append(packageHash.get(package))
        packageHash.get(package).left = truck.departTime

    for package in delivering:
        package.left = truck.departTime

    while len(delivering) > 0:  # while there are still packages to be delivered: deliver packages
        nextMileage = 10
        nextPackage = delivering[0]

        for package in delivering:  # go through each package the truck has

            # get distances to compare to each other
            nextPackageDistance = getDistance(address.index([truck.address]), address.index([nextPackage.address]))
            packageDistance = getDistance(address.index([truck.address]), address.index([package.address]))
            if nextPackageDistance >= packageDistance:  # nearest neighbor algorithm
                nextPackage = package

        nextMileage = getDistance(address.index([truck.address]), address.index([nextPackage.address]))

        truck.mileage += float(nextMileage)  # update truck's mileage

        truck.time += datetime.timedelta(hours=float(nextMileage) / truck.speed)  # update truck's time
        nextPackage.deliveredTime = truck.time  # update the package's delivery time

        packageHash.add(nextPackage.packageID, nextPackage) # update the pack in the packageHash

        delivering.remove(nextPackage)  # remove package from needing to be delivered
        truck.address = nextPackage.address  # update truck's address


address = []  # List for addresses
loadAddressData('address.csv', address)  # address data read into file

distance = []  # List for distances
loadDistanceData('distances.csv', distance)  # address data read into file

packageHash = ChainingHashMap()  # Hash map for packages
loadPackageData('packages.csv')


truck1 = Truck([14, 15, 16, 34, 26, 22, 1, 40, 20, 19 , 21, 33, 4, 13, 30, 37], "4001 South 700 East",
               datetime.timedelta(hours=8))
sendTruck(truck1)  # load and then send truck 1

truck2 = Truck([3, 18, 24, 36, 38, 8, 9, 5, 10, 35, 27, 39, 2],
               "4001 South 700 East", datetime.timedelta(hours=10, minutes=20))
sendTruck(truck2)  # load and then send truck 2

truck3 = Truck([28, 31, 6, 11, 23, 29, 17, 12, 7, 32, 25], "4001 South 700 East",
               datetime.timedelta(hours=9, minutes=5))
sendTruck(truck3)  # load and then send truck 3



class Main:  # Console Menu
    print('Welcome to WGUPS!')  # Welcome message
    text = input('What would you like to see? Type 1 for mileage or 2 for packages, other inputs will terminate the '
                 'program.')
    if text == '1':  # user selcted mileage
        whichMileage = input('Would you like to see all trucks mileage or for 1 truck? Please type all or 1.')

        if whichMileage == 'all':
            print('Truck 1s mileage is: ' + str(truck1.mileage))
            print('Truck 2s mileage is: ' + str(truck2.mileage))
            print('Truck 3s mileage is: ' + str(truck3.mileage))
            print('The total mileage drove by all trucks is: ' + str(truck1.mileage + truck2.mileage + truck3.mileage))
            # prints all truck's mileage
        elif whichMileage == '1':
            whichTruck = input('Which truck? Please type 1, 2, or 3')  # which truck user wants to see
            if whichTruck == '1':
                print(truck1.mileage)  # print truck1's mileage
            elif whichTruck == '2':
                print(truck2.mileage)  # print truck2's mileage
            elif whichTruck == '3':
                print(truck3.mileage)  # print truck3's mileage
    elif text == '2':  # user selected packages
        try:
            time = input('Enter a time. Please type as hh:mm')  # need a tme to use as reference
            (h, m) = time.split(":")
            time = datetime.timedelta(hours=int(h), minutes=int(m))
            truck1.updatePackages(time)
            truck2.updatePackages(time)
            truck3.updatePackages(time)  # update package's status for that time
            whichPackages = input('Type all to see all packages statuses or one to see one')
            if whichPackages == 'one':  # user wants to see only 1 package
                try:
                    packageInput = input("Enter the package ID number")
                    package = packageHash.get(int(packageInput))
                    print("PackageID Address City State ZipCode DeliveryDeadline TimeItLeft Weight Note Status "
                          "DeliveredTime")
                    print(str(package))  # print the selected package
                except ValueError:  # error in input catching
                    print("Invalid input. Terminating program")
                    exit()
            elif whichPackages == "all":
                try:
                    print("PackageID Address City State ZipCode DeliveryDeadline TimeItLeft Weight Note Status "
                          "DeliveredTime")
                    for packageID in range(1, packageHash.size + 1):  # go through the entire packageHash
                        package = packageHash.get(packageID)
                        print(str(package)) # print each package
                except ValueError:  # catch error in input
                    print("Invalid input. Terminating program")
                    exit()
            else:
                exit()
        except ValueError:  # catch error in input
            print("Invalid input. Terminating program")
            exit()
    else:  # catch error in input
        print("Invalid input. Terminating program")
        exit()
