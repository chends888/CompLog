userinput = str(input())
print()

userinput = userinput.replace(' ','')

num_op_list = []
currnum = ''
for i in userinput:
    try:
        int(i)
        currnum = currnum + i
    except:
        num_op_list.append(int(currnum))
        currnum = ''
        num_op_list.append(i)
num_op_list.append(int(currnum))

num1 = num_op_list[0]
num2 = False

for i in range(1, len(num_op_list)):
    if isinstance(num1, str):
        print('Operação inválida')
        break

    if isinstance(num_op_list[i], str):
        op = num_op_list[i]

    if isinstance(num_op_list[i], int):
        num2 = num_op_list[i]

    if op == '+' and num2:
        num1 += num2
        num2 = False
    elif op == '-' and num2:
        num1 -= num2
        num2 = False

print(num1)