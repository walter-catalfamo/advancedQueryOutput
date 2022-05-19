from utils.distance import distance_calculator


def input_reader(string_array, r):
    res = []
    for string in string_array:
        res.append(distance_calculator(string, r, 1)/100)
    return res


threshold = 0.5

values = ["ciao", "cane", "casa"]
values_reference = "caso"
x_input = input_reader(values, values_reference)

attributes = ["director", "newDirector", "actor"]
attributes_reference = "newActor"
w_weights = input_reader(attributes, attributes_reference)


def step(weighted_sum):
    if weighted_sum > threshold:
        return 1
    else:
        return 0


def perceptron():
    weighted_sum = 0
    for x, w in zip(x_input, w_weights):
        weighted_sum += x * w
        print(weighted_sum)
    return step(weighted_sum)


output = perceptron()
print("output " + str(output))
