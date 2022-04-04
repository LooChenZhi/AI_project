# Import Libraries
from random import randint
import random

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


# Individual Function
st.title("Question 1: Vacation Planner")
st.markdown("Using Genetic Algorithm (GA) to solve a vacation planning. The goal is to optimize the vacation experience with a fixed amount of money and fixed duration. This application will generate the best combination of values for each parameter.")

st.sidebar.header("Change the values here")
money_on_hand = st.sidebar.slider("Money On-Hand (RM)", min_value = 4000, max_value = 10000, value = 1000, step = 1000)
duration = st.sidebar.slider("Duration (Day)", min_value = 3, max_value = 10, value = 3, step = 1)
p_count = st.sidebar.slider("Population", min_value = 100, max_value = 1000, value = 100, step = 100)
n_generation = st.sidebar.slider("Generation", min_value = 100, max_value = 1000, value = 200, step = 100)
data = {"Budget" : money_on_hand,
        "Duration" : duration,
        "population" : p_count,
        "n_generation" : n_generation}

money_on_hand = int(money_on_hand) #budget
duration = int(duration)
p_count = int(p_count)
n_generation = int(n_generation)

# Create an individual list. An individual is a member of a population.
# Range each parameter
def individual():
    hotel = random.randint(100,500)
    t_spots = random.randint(2, 10)
    one_t_spots = random.randint(5, 300)
    food_per_meals = random.randint(10, 100)
    t_fee = random.randint(5, 100)
    t_fre = random.randint(1,10)
     
    return [hotel,food_per_meals,t_spots,one_t_spots,t_fee,t_fre] 
          #[HotelBudget,FoodBudget,TouristSpots,OneTouristSpots,TransportFees,Transport Frequency]


# Population function
# Create population contains individuals
# The collection of all individuals is referred to as our population.
def population(count):
    return [individual() for x in range(count)]


# Fitness function
# Count the fitness function for an individual
# Calculate the range between money on hand with total
def fitness(individual):
    # [hotel,food_per_meals,t_spots,one_t_spots,t_fee,t_fre]
    total = individual[0]*4 + individual[1]*3*duration + individual[2]*individual[3] + individual[4]*individual[5]*duration
    return abs(money_on_hand - total)


# Average fitness function

# Calculate the fitness function to retrieve average fitness for a population
def average_fitness(pop):
    summed = [fitness(i) for i in pop]
    return (sum(summed) / len(pop))


# Evolution Function
def evolve(pop, retain, crossover1, crossover2, mutate, random_select = 0.05):
    
    graded = [(fitness(x), x) for x in pop]
    sort_graded = [x[1]for x in sorted(graded)]  # x [1] because x has two component, just take the list --> e.g. [(50,[41,38,86,30,55])]
    retain_length = int(len(sort_graded)*retain) # how many top % parents to be remainded
    parents = sort_graded[0:retain_length] # get the list of array of individuals as parents - after sorted

    # randomly add other individuals to promote genetic diversity
    for individual in sort_graded[retain_length:]: # get from the remaining individuals NOT selected as parents initially !
        if random_select > random.random():
            parents.append(individual)

    # mutate some individuals
    for individual in parents:
        if mutate > random.random():
            pos_to_mutate =randint(0, len(individual) - 1)
            individual[pos_to_mutate] = randint(min(individual), max(individual))

    # crossover parents to create children
    parents_length = len(parents)
    desired_length = len(pop) - parents_length
    children = []
    while len(children) < desired_length:
        male = randint(0, parents_length - 1)
        female = randint(0, parents_length - 1)
        if male != female:
            male = parents[male]
            female = parents[female]
            half = int(len(male)/2)
            child = male[:crossover1] + female[crossover2:]
            children.append(child)
    parents.extend(children)
    
    return parents


def gen():
    # Result
    # Decalaration of list
    value_lst =[]
    fitness_history = []

    p = population(p_count)

    # Iterate and modeling for result
    for i in range(n_generation):
        p = evolve(p, retain, crossover1, crossover2, mutate)
        value = average_fitness(p)
        fitness_history.append(value)
        value_lst.append(p[0])
        value_lst.append(value)

    #st.write(value_lst) #print result

    best_model = value_lst[-2]
    best_fit = value_lst[-1]


    # [hotel,food,t_spots,one_t_spots,t_fee,t_fre]
    st.write("**Best Solution :**")
    st.write("Money on hand       = RM",money_on_hand)
    st.write("Vacation duration   =",duration,"days")
    st.write("Hotel Price         = RM", best_model[0])
    st.write("Food Price          = RM", best_model[1],"per meal")
    st.write("Travel Spot         =",best_model[2],"spots")
    st.write("One Spot Price      = RM", best_model[3])
    st.write("Transport Fee       = RM", best_model[4])
    st.write("Transport Frequency =", best_model[5],"trip per day")


    total = best_model[0]*4 + best_model[1]*3*duration + best_model[2]*best_model[3] + best_model[4]*best_model[5]*duration
    st.write("Total expenses: RM", total)

    df_hist = pd.DataFrame()
    df_hist["Generation"] = [x + 1 for x in list(range(len(fitness_history)))]
    df_hist["Fitness History"] = fitness_history

    return fitness_history, best_fit, df_hist

st.write("# Method 1")
retain = 0.2
mutate = 0.02
crossover1 = 2
crossover2 = 2
st.write("Selection: 20%")
st.write("Mutate Position: 2")
st.write("From Male: First 2")
st.write("From Female: Last 2")
st.write(" ")
hist1, fit1, df1 = gen()
st.markdown("""---""")

st.write("# Method 2")
retain = 0.4
mutate = 0.04
crossover1 = 4
crossover2 = 4
st.write("Selection: 40%")
st.write("Mutate Position: 4")
st.write("From Male: First 4")
st.write("From Female: Last 4")
st.write(" ")
hist2, fit2, df2 = gen()
st.markdown("""---""")

st.write("# Method 3")
retain = 0.1
mutate = 0.01
crossover1 = 1
crossover2 = 1
st.write("Selection: 10%")
st.write("Mutate Position: 1")
st.write("From Male: First 1")
st.write("From Female: Last 1")
st.write(" ")
hist3, fit3, df3 = gen()
st.markdown("""---""")

st.write("# Compare the Results")
merged_df = pd.merge(df2, df3, how = "outer", on = ["Generation"])
merged_df = pd.merge(merged_df, df1, how = "outer", on = ["Generation"])
merged_df.columns = ["Generation", "Method 1", "Method 2", "Method 3"]
merged_df
st.write(" ")

#Plot graph
fig, ax = plt.subplots(figsize = (10, 5))

plt.plot(hist1, label = "Method 1")
plt.plot(hist2, label = "Method 2")
plt.plot(hist3, label = "Method 3")
plt.legend()

ax.set_xlabel("Generation")
ax.set_ylabel("Fitness")
ax.set_title("Fitness over Generation")
st.pyplot(fig)
