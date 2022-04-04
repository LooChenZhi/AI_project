#!/usr/bin/env python
# coding: utf-8

# # Question 1 : Vacation Planner

# Import Libraries

# In[ ]:


from random import randint
import random

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


# Individual Function

# In[ ]:


money_on_hand = 5000    #budget
duration = 5            #5days4night

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

# In[ ]:


# Create population contains individuals
# The collection of all individuals is referred to as our population.
def population(count):
    return [individual() for x in range(count)]


# Fitness function

# In[ ]:


# Count the fitness function for an individual
# Calculate the range between money on hand with total
def fitness(individual):
    # [hotel,food_per_meals,t_spots,one_t_spots,t_fee,t_fre]
    total = individual[0]*4 + individual[1]*3*duration + individual[2]*individual[3] + individual[4]*individual[5]*duration
    return abs(money_on_hand - total)


# Average fitness function

# In[ ]:


# Calculate the fitness function to retrieve average fitness for a population
def average_fitness(pop):
    summed = [fitness(i) for i in pop]
    return (sum(summed) / len(pop))


# Evolution Function

# In[ ]:


def evolve(pop, retain = 0.2, random_select = 0.05, mutate = 0.01):
    
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
            child = male[:half] + female[half:]
            children.append(child)
    parents.extend(children)
    
    return parents


# Result

# In[ ]:


# Decalaration of list
value_lst =[]
fitness_history = []

p_count = 100
n_generation = 100

p = population(p_count)

# Iterate and modeling for result
for i in range(n_generation):
    p = evolve(p)
    value = average_fitness(p)
    fitness_history.append(value)
    value_lst.append(p[0])
    value_lst.append(value)

st.write(value_lst) #print result


# In[ ]:


best_model = value_lst[-2]

def best_solution():
    # [hotel,food,t_spots,one_t_spots,t_fee,t_fre]
    st.write("Best Solution :")
    st.write("Money on hand       = RM",money_on_hand)
    st.write("Vacation duration   =",duration,"days")
    st.write("Hotel Price         = RM", best_model[0])
    st.write("Food Price          = RM", best_model[1],"per meal")
    st.write("Travel Spot         =",best_model[2],"spots")
    st.write("One Spot Price      = RM", best_model[3])
    st.write("Transport Fee       = RM", best_model[4])
    st.write("Transport Frequency =", best_model[5],"trip per day")

best_solution()


# In[ ]:


total = best_model[0]*4 + best_model[1]*3*duration + best_model[2]*best_model[3] + best_model[4]*best_model[5]*duration
st.write("Total expenses: RM", total)


# Plotting Chart

# In[ ]:


xval = np.arange(1, 101)
yval = fitness_history

fig = plt.figure(figsize=(20,10))
plt.subplot(122)
plt.axhline(y=0, color='r', linestyle='-')
plt.plot(yval, color='c')
plt.xlim(-5)

plt.xlabel('Number of generation')
plt.ylabel('Fitness')
plt.title('Fitness vs Number of generation')
st.pyplot(fig)


# <a style='text-decoration:none;line-height:16px;display:flex;color:#5B5B62;padding:10px;justify-content:end;' href='https://deepnote.com?utm_source=created-in-deepnote-cell&projectId=158f0e5f-0c09-4da4-a8e2-16b96f03a497' target="_blank">
# <img alt='Created in deepnote.com' style='display:inline;max-height:16px;margin:0px;margin-right:7.5px;' src='data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB3aWR0aD0iODBweCIgaGVpZ2h0PSI4MHB4IiB2aWV3Qm94PSIwIDAgODAgODAiIHZlcnNpb249IjEuMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayI+CiAgICA8IS0tIEdlbmVyYXRvcjogU2tldGNoIDU0LjEgKDc2NDkwKSAtIGh0dHBzOi8vc2tldGNoYXBwLmNvbSAtLT4KICAgIDx0aXRsZT5Hcm91cCAzPC90aXRsZT4KICAgIDxkZXNjPkNyZWF0ZWQgd2l0aCBTa2V0Y2guPC9kZXNjPgogICAgPGcgaWQ9IkxhbmRpbmciIHN0cm9rZT0ibm9uZSIgc3Ryb2tlLXdpZHRoPSIxIiBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPgogICAgICAgIDxnIGlkPSJBcnRib2FyZCIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTEyMzUuMDAwMDAwLCAtNzkuMDAwMDAwKSI+CiAgICAgICAgICAgIDxnIGlkPSJHcm91cC0zIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgxMjM1LjAwMDAwMCwgNzkuMDAwMDAwKSI+CiAgICAgICAgICAgICAgICA8cG9seWdvbiBpZD0iUGF0aC0yMCIgZmlsbD0iIzAyNjVCNCIgcG9pbnRzPSIyLjM3NjIzNzYyIDgwIDM4LjA0NzY2NjcgODAgNTcuODIxNzgyMiA3My44MDU3NTkyIDU3LjgyMTc4MjIgMzIuNzU5MjczOSAzOS4xNDAyMjc4IDMxLjY4MzE2ODMiPjwvcG9seWdvbj4KICAgICAgICAgICAgICAgIDxwYXRoIGQ9Ik0zNS4wMDc3MTgsODAgQzQyLjkwNjIwMDcsNzYuNDU0OTM1OCA0Ny41NjQ5MTY3LDcxLjU0MjI2NzEgNDguOTgzODY2LDY1LjI2MTk5MzkgQzUxLjExMjI4OTksNTUuODQxNTg0MiA0MS42NzcxNzk1LDQ5LjIxMjIyODQgMjUuNjIzOTg0Niw0OS4yMTIyMjg0IEMyNS40ODQ5Mjg5LDQ5LjEyNjg0NDggMjkuODI2MTI5Niw0My4yODM4MjQ4IDM4LjY0NzU4NjksMzEuNjgzMTY4MyBMNzIuODcxMjg3MSwzMi41NTQ0MjUgTDY1LjI4MDk3Myw2Ny42NzYzNDIxIEw1MS4xMTIyODk5LDc3LjM3NjE0NCBMMzUuMDA3NzE4LDgwIFoiIGlkPSJQYXRoLTIyIiBmaWxsPSIjMDAyODY4Ij48L3BhdGg+CiAgICAgICAgICAgICAgICA8cGF0aCBkPSJNMCwzNy43MzA0NDA1IEwyNy4xMTQ1MzcsMC4yNTcxMTE0MzYgQzYyLjM3MTUxMjMsLTEuOTkwNzE3MDEgODAsMTAuNTAwMzkyNyA4MCwzNy43MzA0NDA1IEM4MCw2NC45NjA0ODgyIDY0Ljc3NjUwMzgsNzkuMDUwMzQxNCAzNC4zMjk1MTEzLDgwIEM0Ny4wNTUzNDg5LDc3LjU2NzA4MDggNTMuNDE4MjY3Nyw3MC4zMTM2MTAzIDUzLjQxODI2NzcsNTguMjM5NTg4NSBDNTMuNDE4MjY3Nyw0MC4xMjg1NTU3IDM2LjMwMzk1NDQsMzcuNzMwNDQwNSAyNS4yMjc0MTcsMzcuNzMwNDQwNSBDMTcuODQzMDU4NiwzNy43MzA0NDA1IDkuNDMzOTE5NjYsMzcuNzMwNDQwNSAwLDM3LjczMDQ0MDUgWiIgaWQ9IlBhdGgtMTkiIGZpbGw9IiMzNzkzRUYiPjwvcGF0aD4KICAgICAgICAgICAgPC9nPgogICAgICAgIDwvZz4KICAgIDwvZz4KPC9zdmc+' > </img>
# Created in <span style='font-weight:600;margin-left:4px;'>Deepnote</span></a>
