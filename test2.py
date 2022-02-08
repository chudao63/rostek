# import redis
# from app import redisClient

# numberList = "numbers"
# redisClient.rpush(numberList, 2,4,6,8,10,12)
# # Trim the list to have only single digit elements

# startIndex  = 0
# endIndex    = 3
# newList     = redisClient.ltrim(numberList, startIndex, endIndex)
# # Print the Redis list after trimming
# print("Single digit even numbers:")
# for i in range(0, redisClient.llen(numberList)):
#     print(redisClient.lindex("numbers",i))
# # Clear the Redis list
# for i in range(0, redisClient.llen(numberList)):
#     redisClient.lpop(numberList)
import tailer
from app import mqtt


# print(tailer.tail(open('logs/user_log.log')),1)

print(tailer.tail(open('logs/user_log.log'), 1))
# for line in tailer.tail(open('logs/user_log.log'),1):
#     print(line)



