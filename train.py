#The first thing to do is to import the relevant packages
# that I will need for my script, 
#these include the Numpy (for maths and arrays)
#and csv for reading and writing csv files
#If i want to use something from this I need to call 
#csv.[function] or np.[function] first

import csv as csv 
import numpy as np

#Open up the csv file in to a Python object
csv_file_object = csv.reader(open('train.csv', 'rb')) 
header = csv_file_object.next()  #The next() command just skips the 
                                 #first line which is a header
data=[]                          #Create a variable called 'data'
for row in csv_file_object:      #Run through each row in the csv file
	data.append(row)             #adding each row to the data variable
data = np.array(data) 	         #Then convert from a list to an array
number_passengers = np.size(data[0::,0].astype(np.float))

number_passengers = np.size(data[0::,0].astype(np.float))
number_survived = np.sum(data[0::,0].astype(np.float))
proportion_survivors = number_survived / number_passengers

women_only_stats = data[0::,3] == "female"
men_only_stats = data[0::,3] != "female"

print number_passengers
print number_survived
print proportion_survivors
print len(women_only_stats)
print len(men_only_stats)

#Using the index from above we select the females and males separately
women_onboard = data[women_only_stats,0].astype(np.float)     
men_onboard = data[men_only_stats,0].astype(np.float)

# Then we finds the proportions of them that survived
proportion_women_survived = np.sum(women_onboard) / np.size(women_onboard)  
proportion_men_survived = np.sum(men_onboard) / np.size(men_onboard) 

#and then print it out
print 'Proportion of women who survived is %s' % proportion_women_survived
print 'Proportion of men who survived is %s' % proportion_men_survived

test_file_obect = csv.reader(open('train.csv', 'rb'))
header = test_file_obect.next()

open_file_object = csv.writer(open("genderbasedmodelpy.csv", "wb"))
for row in test_file_obect:       #for each row in test.csv
    if row[2] == 'female':             #is it a female, if yes then
        row.insert(0,'1')              #then Insert the prediction
                                       #of survived,'1' at position 0 
        open_file_object.writerow(row) #and write the row to the
    else:                              #new file else
        row.insert(0,'0')	       #insert the prediction of did not 
        open_file_object.writerow(row) #survive (0) and write row

fare_ceiling = 40
data[data[0::,8].astype(np.float) >= fare_ceiling, 8] = fare_ceiling-1.0
fare_bracket_size = 8
number_of_price_brackets = fare_ceiling / fare_bracket_size
number_of_classes = 2 #There were 1st, 2nd and 3rd classes on board 
# Define the survival table
survival_table = np.zeros((2, 2, number_of_price_brackets))

# I can now find the stats of all the women and men on board
for i in xrange(number_of_classes):
	for j in xrange(number_of_price_brackets):

		women_only_stats = data[ (data[0::,3] == "female") \
                                 & (data[0::,4].astype(np.int) >= 10) \
                                 & (data[0:,8].astype(np.float) >= j*fare_bracket_size) \
                                 & (data[0:,8].astype(np.float) < (j+1)*fare_bracket_size), 0]

        men_only_stats = data[ (data[0::,3] != "female") \
                                 & (data[0::,4].astype(np.int) >= 10) \
                                 & (data[0:,8].astype(np.float) >= j*fare_bracket_size) \
                                 & (data[0:,8].astype(np.float) < (j+1)*fare_bracket_size), 0]

                                 #if i == 0 and j == 3:
        survival_table[0,i,j] = np.mean(women_only_stats.astype(np.float)) #Women stats
        survival_table[1,i,j] = np.mean(men_only_stats.astype(np.float)) #Men stats

#Since in python if it tries to find the mean of an array with nothing in it
#such that the denominator is 0, then it returns nan, we can convert these to 0
#by just saying where does the array not equal the array, and set these to 0.
survival_table[ survival_table != survival_table ] = 0.

#Now I have my proportion of survivors, simply round them such that if <0.5
#they dont surivive and >1 they do
survival_table[ survival_table < 0.5 ] = 0
survival_table[ survival_table >= 0.5 ] = 1


#Now I have my indicator I can read in the test file and write out
#if a women then survived(1) if a man then did not survived (0)
#1st Read in test
test_file_obect = csv.reader(open('test.csv', 'rb'))
open_file_object = csv.writer(open("genderclasspricebasedmodelpy.csv", "wb"))

header = test_file_obect.next()

#First thing to do is bin up the price file
for row in test_file_obect:
    if int(row[4]) >= 10:
        malutek = 0
    else:
        malutek = 1

    for j in xrange(number_of_price_brackets):
        #If there is no fare then place the price of the ticket
        #according to class
        try:
            row[7] = float(row[7]) #No fare recorded will come up as a string so
                                    #try to make it a float
        except: #If fails then just bin the fare according to the class
            bin_fare = 3-float(row[0])
            break #Break from the loop and move to the next row
        if row[7] > fare_ceiling: #Otherwise now test to see if it is higher
                                  #than the fare ceiling we set earlier
            bin_fare = number_of_price_brackets-1
            break #And then break to the next row

        if row[7] >= j*fare_bracket_size\
            and row[7] < (j+1)*fare_bracket_size:#If passed these tests then loop through
                                          #each bin until you find the right one
                                          #append it to the binned_price
                                          #and move to the next loop
            bin_fare = j
            break
        #Now I have the bin fare, the class and whether female or male we can
        #just cross ref their details with our 'survivial table
    if row[2] == 'female':
        row.insert(0,int(survival_table[0,malutek,bin_fare])) #Insert the prediciton
                                                        #at the start of the row
        open_file_object.writerow(row) #Write the row to the file
    else:
        row.insert(0,int(survival_table[1,malutek,bin_fare])) #Insert the prediciton
                                                        #at the start of the row
        open_file_object.writerow(row)
































