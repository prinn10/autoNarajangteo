test_list = [1, 3, 4, 3, 6, 7]
print("Original list : " + str(test_list))
res_list = list(filter(lambda x: test_list[x] == 3, range(len(test_list))))
print("New indices list : " + str(res_list))

for i in res_list[1:]:
    del test_list[i]

print(test_list)