# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 10:23:24 2017
Visualization of the results
@author: cheng
"""

import numpy as np
#import matplotlib
#matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import animation
import pickle
from matplotlib import style



def get_plot_trajectories(true_trajs, pred_trajs, obs_length, name):
    '''
    Functions that plot the true trajectories and predicted trajectories
    params:
        true_trajs: numpy matrix with points of the true trajectoies with shape (traj_length x maxNumUsers x 4)
        pred_trajs: numpy matrix with points of the predicted trajectories with shape (traj_length x maxNumUsers x 4)
        obs_length: length of the observed trajectory
        name: name of the plot    
    '''
    # Get the shape of trajectory (traj_length x maxNumUsers x 4)
    traj_length, maxNumUsers, _ = true_trajs.shape
    
    
    # Load the background
    # Read background image


#    im = plt.imread('background_Bergedorf.png')
#    # Plot image
#    #implot = plt.imshow(im)
#    # Get image size
#    width = im.shape[0]
#    height = im.shape[1]
    
#    # Ploting without background image
    width = 100
    height = 100

    # Define a dictionary  traj_data to store the trajectory
    # traj_data.index: user index
    # traj_data.value: it is a list with to element -- true position, and predicted position, with the length of traj_length
    traj_data = {}
    
    #  each frame/each point in all trajectories
    for i in range(traj_length):
        pred_pos = pred_trajs[i, :]
        true_pos = true_trajs[i, :]
        
        # For each user
        for j in range(maxNumUsers):
            # Check the userId
            if true_pos[j, 0] == 0:
                # Not a user
                continue
            elif pred_pos[j, 0] == 0:
                # Not a user
                continue
            else:
                # If he or she is a user but out of the define area, this user will not be plot
                if true_pos[j, 1] > 1 or true_pos[j, 1] < 0:
                    continue
                elif true_pos[j, 2] > 1 or true_pos[j, 2] < 0:
                    continue
                # user trajectories will be empty is the user index is not in traj_data and i is less than obs_length
                if (j not in traj_data) and i < obs_length:
                    traj_data[j] = [[], []]
                    
                # Accumulate the trajectory sequence alone the user for valid trajectory
                # true_pos[j, 1:4]: x, y, userType
                if j in traj_data:
                    traj_data[j][0].append(true_pos[j, 1:4])
                    traj_data[j][1].append(pred_pos[j, 1:4])
                    
    # Plot trajectory user by user in this traj_data
    traj_seq = []
    for j in traj_data:
        true_pos_user = traj_data[j][0]
        pred_pos_user = traj_data[j][1]
        
        # Convert the x and y coordinates back to background size
        true_x = [p[0]*height for p in true_pos_user]
        true_y = [p[1]*width for p in true_pos_user]
#        userType = true_pos_user[0][2]
        pred_x = [p[0]*height for p in pred_pos_user]
        pred_y = [p[1]*width for p in pred_pos_user]
        traj_seq.append([[true_x, true_y], [pred_x, pred_y]])
        
                   
    return traj_seq
    
style.use('seaborn-poster')

# Set up formatting for the movie files
Writer = animation.writers['ffmpeg']
writer = Writer(fps=1, metadata=dict(artist='Me'), bitrate=1800)

print(plt.style.available)
    
#im = plt.imread('background_Bergedorf.png')
#    # Plot image
##implot = plt.imshow(im)
#    # Get image size
#width = im.shape[0]
#height = im.shape[1]
    

# Load the results of the model
f = open('data\modelingTrajectories.pkl', 'rb')
results = pickle.load(f)
        
        
name = 'sequence' + str(0)
traj_seq = get_plot_trajectories(results[166][0], results[166][1], results[166][2], name)
#print(np.asarray(traj_seq).shape)
#traj_seq = np.asarray(traj_seq)
#traj_seq = np.reshape(traj_seq, (-1, 2))
#print(np.asarray(traj_seq).shape)
print(len(traj_seq))
for data in traj_seq:
    print(data, '\n')
    
print('************************************')
frame_seq = []    
for data in traj_seq:
    for d in data:
        # Only save sequence = 12
        if len(d[0]) == 12:
            print(d, '\n')
            frame_seq.append(d)
print(frame_seq)
print('************************************')
    
fig = plt.figure()
ax1 = plt.axes(xlim=(25, 90), ylim=(10, 60))
#ax1 = plt.axes(xlim=(0, 100), ylim=(0, 100))
line, = ax1.plot([], [], lw=2)
plt.xlabel('X-coordinate')
plt.ylabel('Y-coordinate')


# fake data
frame_num = 12
#gps_data =  traj_seq.tolist()
gps_data = frame_seq
#gps_data = gps_data.tolist()
for user_seq in gps_data:
    print(user_seq, '\n')



c = np.random.rand(3, 1)
c1 = [c[0], c[1]*0.8, c[2]*0.5]

#plotlays, plotcols = [2], ['k', 'r']
plotlays = [2]
plotcols = ['k','#f8551f','k','#3f9d7b','k','#be31df','k','#66b5d9','k','#f31b63','k','#50e8bd',
            'k','#ccff00','k','#48b0bf','k','#94e628','k','#0468c8','k','#66cdaa','k','#ad0673',
            'k','#04eb87','k','#2abddc','k','#31698a','k','#f8013b','k','#04cba9','k','#adb6d9',
            'k','#ff7f50','k','#94e628','k','#5789de','k','#31698a','k','#9c5279','k','#ff00ff',
            'k','b','k','g','k','r','k','c','k','m','k','y',
            'k','b','k','g','k','r','k','c','k','m','k','y',
            'k','b','k','g','k','r','k','c']
lines = []
for index in range(len(frame_seq)):
    if index % 2 == 0:
        lobj = ax1.plot([],[], lw=2, color=plotcols[index], linestyle='dashdot', marker='<', markersize=5)[0] # line object -- get the first element
    elif index % 2 == 1:
        lobj = ax1.plot([],[], lw=2, color=plotcols[index], alpha=0.75, linestyle='dashed', marker='o', markersize=5)[0]
    else:
        continue
    lines.append(lobj) # lines is a list containing line objects


def init():
    for line in lines:
        line.set_data([],[]) # Initialize the data for each line object
    return lines

x_pos = [[] for i in range(len(frame_seq))]
y_pos = [[] for i in range(len(frame_seq))]


def animate(i):
    for n in range(len(frame_seq)):
        x = gps_data[n][0][i]
        y = gps_data[n][1][i]
        x_pos[n].append(x)
        y_pos[n].append(y)
    
    for lnum, line in enumerate(lines):
        line.set_data(x_pos[lnum], y_pos[lnum])

    return lines

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=frame_num, interval=1500, blit=False, repeat=False)

plt.title('Trajectory Modeling in Shared Spaces')
plt.plot([],[], color=plotcols[0], linestyle='dashdot', marker='<', markersize=5, label='Observation')
plt.plot([],[], color=plotcols[0], linestyle='dashed', marker='o', markersize=5, label='Prediction \n(color-coded)')
plt.legend()
plt.grid(True)
plt.show()
anim.save('seq_166.mp4', writer=writer)
#anim.save('seq_41.gif', dpi=80, writer='ffmpeg')    

    
        
        
                
            
        
    


