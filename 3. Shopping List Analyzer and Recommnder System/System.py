'''
    This project analyzes a dataset of shopping lists and offers
product recommendations based on popularity and user preferences.
Here's a summary of the key functionalities:

-Graph-Based Algorithm:
The algorithmic thinking behind this system involves a bipartite graph approach to analyze shopping preferences and provide personalized recommendations.
The data, representing customer shopping lists, can be viewed as a bipartite graph with two sets of nodes: customers and products.
The edges connect customers to the products they have purchased. The Counter function is used to count the occurrences of each product,
effectively measuring its popularity across all customers. The script then identifies the "hottest" products based on their frequency.
When a user makes a choice, the system traverses the graph to find other products frequently co-purchased with the user's choice.
This is achieved by checking the shopping lists of customers who have purchased the same product.
The final step involves counting the occurrences of these co-purchased products and presenting the top three recommended items.
The algorithm demonstrates a graph-based approach to uncovering product associations and delivering personalized suggestions.

-Data Structure (Dictionary):
Utilizes a dictionary to represent shopping lists associated with unique customer IDs.

-Product Occurrence Counting:
Uses the Counter class from the collections module to count the occurrences of each product across all shopping lists.

-Sorting and Display:
Sorts the products based on their occurrence counts in descending order.
Prints the top three most frequently occurring products as the "hottest products."

-User Input and Recommendation:
Takes user input for their preferred product.
Recommends three products that frequently appear in shopping lists along with the user's choice.
'''

from collections import Counter

data = {
    "10001": ["cake", "cheese", "milk", "eggs", "bread"],
    "10002": ["apples", "bananas", "yogurt", "chicken", "rice", "cake"],
    "10003": ["cookies", "soda", "chips", "ice cream"],
    "10004": ["spinach", "tomatoes", "onions", "garlic"],
    "10005": ["coffee", "tea", "sugar", "flour", "butter"],
    "10006": ["chocolate", "crackers", "apples", "chicken", "pasta"],
    "10007": ["ice cream", "bread", "milk", "spinach", "cookies"],
    "10008": ["rice", "cheese", "tomatoes", "soda", "bananas"],
    "10009": ["butter", "garlic", "eggs", "cake", "tea"],
    "10010": ["yogurt", "coffee", "sugar", "flour", "chips"]
}

# Count the occurrences of each product
product_counts = Counter(product for products in data.values() for product in products)
sorted_product_counts = sorted(product_counts, key=lambda k: product_counts[k], reverse=True)

# Display the hottest products
print("hottest products:")
for i in range(0,3):
    print(sorted_product_counts[i])

print('\n')
          
choice = input("Give your choice : ")
print("\n   Good Choice!\n")

recommended_values=[]

for key, value in data.items():
    if choice in value:
        for val in value:
            if val!=choice:
                recommended_values.append(val)

recommended_values = set(recommended_values)

best_values={}

for recommend in recommended_values:
    count = 0
    for key, value in data.items():
        count += (value.count(recommend))

    best_values.update({recommend : count})
    
sorted_recommends = sorted(best_values, key=lambda k: best_values[k], reverse=True)

print("recommendeds:")
for i in range(0,3):
    print(sorted_recommends[i])
    
print("\n")
    