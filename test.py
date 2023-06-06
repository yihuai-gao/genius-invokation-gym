

test_list = ["a","b","c","d","e","f","g"]

for idx in range(len(test_list)-1,-1,-1):
    words = test_list[idx]
    print(words)
    if words == "e":
        test_list.pop(idx)
        
print(test_list)