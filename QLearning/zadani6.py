
import gym
import random

random.seed(1234)

streets = gym.make("Taxi-v3").env #New versions keep getting released; if -v3 doesn't work, try -v2 or -v4
streets.render()

initial_state = streets.encode(2, 3, 2, 0)

streets.s = initial_state

streets.render()

import numpy as np

q_table = np.zeros([streets.observation_space.n, streets.action_space.n])
# a 2D array that represent every possible state and action in the virtual space and initialize all of them to 0
learning_rate = 0.1
discount_factor = 0.6
exploration = 0.1
epochs = 10000

for taxi_run in range(epochs):
    state = streets.reset()
    done = False
    
    while not done:
        random_value = random.uniform(0, 1)
        if (random_value < exploration):
            action = streets.action_space.sample() # Explore a random action
        else:
            action = np.argmax(q_table[state]) # Use the action with the highest q-value
            
        next_state, reward, done, info = streets.step(action)
        
        prev_q = q_table[state, action]
        next_max_q = np.max(q_table[next_state])
        new_q = (1 - learning_rate) * prev_q + learning_rate * (reward + discount_factor * next_max_q)
        q_table[state, action] = new_q
        
        state = next_state


from IPython.display import clear_output
from time import sleep
lengths=[]
for tripnum in range(1, 11):
    state = streets.reset()
   
    done = False
    trip_length = 0
    
    while not done and trip_length < 25:
        action = np.argmax(q_table[state])
        next_state, reward, done, info = streets.step(action)
        clear_output(wait=True)
        print("Trip number " + str(tripnum) + " Step " + str(trip_length))
        print(streets.render(mode='ansi'))
        sleep(.2)
        state = next_state
        trip_length += 1
    lengths.append(trip_length)
    
    sleep(.2)
avg_len=sum(lengths)/10
print(avg_len)