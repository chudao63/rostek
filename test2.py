import redis
from app import redisClient


# Sample Python program to demonstrate List operations of Redis

# and redis-py


 

# Create a redis client



# Create a Redis list with few even numbers

numberList = "numbers"

redisClient.rpush(numberList, 2,4,6,8,10,12)

 
# Trim the list to have only single digit elements

startIndex  = 0

endIndex    = 3

newList     = redisClient.ltrim(numberList, startIndex, endIndex)

 
# Print the Redis list after trimming

print("Single digit even numbers:")

for i in range(0, redisClient.llen(numberList)):

    print(redisClient.lindex("numbers",i))


# Clear the Redis list
for i in range(0, redisClient.llen(numberList)):

    redisClient.lpop(numberList)