from maze_env import Maze
from RL_brain import Agent
import time
import random
from  matplotlib import pyplot as plt

alpha=0.8
gamma=0.8
MAZE_H=6
MAZE_W=6

eating=False


if __name__ == "__main__":
    ### START CODE HERE ###
    # This is an agent with random policy. You can learn how to interact with the environment through the code below.
    # Then you can delete it and write your own code.
    Q_value = []
    Q_value1 = []
    Model = []
    Model1 = []
    visited = []
    visited1 = []
    episode_list=[]
    step_list=[]
    episode_rewards=[]
    episode1 = 0

    for i in range(6):
        Q_value.append([])
        Q_value1.append([])
        Model.append([])
        Model1.append([])
        for j in range(6):
            Q_value[i].append([0, 0, 0, 0, 0.1, 0.1, 0.1, 0.1]) # up,down,right,left value and times
            Q_value1[i].append([0, 0, 0, 0, 0.1, 0.1, 0.1, 0.1])  # up,down,right,left value and times
            Model[i].append([0,0,0,0,0,0])  # up down right left reward state_visitedi,j 的reward
            Model1[i].append([0,0,0,0,0,0])
    env = Maze()
    agent = Agent(actions=list(range(env.n_actions)))
    for episode in range(120):
        s = env.reset()
        episode_reward = 0
        step=0
        eating=False
        while True:
            step+=1
            if step>250:
                break
            if eating==False:
                #env.render()                 
               # time.sleep(0.01)
                a = agent.choose_action(s,Q_value,episode,eating)
                s_, r, done = env.step(a)
                s0=int(s[0]/40)
                s1=int(s[1]/40)
                s_0=int(s_[0]/40)
                s_1=int(s_[1]/40)
                #开始学习
                Model[s_0][s_1][4]=r#状态的立即回报 只有个别方块不为0
                if episode>50:
                    Model[s0][s1][5]=1
                    Model[s0][s1][a]=1
                    if [s0, s1, a] not in visited:
                        visited.append([s0, s1, s_0, s_1, a])
                Q_value[s0][s1][a+4]+=1
                if done:
                    if r==-1:
                        Q_value[s0][s1][a]-=10
                    value=r
                else:
                    value=r+gamma*max(Q_value[s_0][s_1][:4])
                Q_value[s0][s1][a]=(1-alpha)*Q_value[s0][s1][a]+alpha*value
                episode_reward += r
                s = s_
                eating=s[4]
                if done:
                    #env.render()
                    time.sleep(0.5)
                    break
                if episode >= 50 and len(visited)>10:
                    for times in range(30*(len(visited)-10)):
                        s1 = [random.randint(0, 5), random.randint(0, 5)]
                        while Model[s1[0]][s1[1]][5] == 0:
                            s1 = [random.randint(0, 5), random.randint(0, 5)]
                        #a = random.choice([opt for opt in [0, 1, 2, 3] if Model[s1[0]][s1[1]][opt] == 1])
                        a = agent.choose_action(s, Q_value, episode,
                                                eating)  # random.choice([opt for opt in [0, 1, 2, 3] if Model1[s1[0]][s1[1]][opt] == 1])
                        if Model[s1[0]][s1[1]][a] == 0:
                            random.choice([opt for opt in [0, 1, 2, 3] if Model[s1[0]][s1[1]][opt] == 1])
                        if a == 0:
                            s2 = [s1[0], s1[1] - 1]
                        elif a == 1:
                            s2 = [s1[0], s1[1] + 1]
                        elif a == 2:
                            s2 = [s1[0] + 1, s1[1]]
                        else:
                            s2 = [s1[0] - 1, s1[0]]
                        if s2[0] >= 0 and s2[0] < 6 and s2[1] >= 0 and s2[1] < 6:
                            r_new = Model[s2[0]][s2[1]][4]
                            Q_value[s1[0]][s1[1]][a] += alpha * (
                                        r_new + gamma * max(Q_value[s2[0]][s2[1]][:4])
                                        - Q_value[s1[0]][s1[1]][a])


            else:
                #env.render()  # You can comment all render() to turn off the graphical interface in training process to accelerate your code.
              #  time.sleep(0.01)
                a = agent.choose_action(s, Q_value1, episode1,eating)
                s_, r, done = env.step(a)
                s0 = int(s[0] / 40)
                s1 = int(s[1] / 40)
                s_0 = int(s_[0] / 40)
                s_1 = int(s_[1] / 40)
                # 开始学习
                Model1[s_0][s_1][4] = r
                if episode1>50:
                    Model1[s0][s1][5] =1
                    Model1[s0][s1][a]=1
                    if [s0, s1, a] not in visited1:
                        visited1.append([s0, s1, s_0, s_1, a])
                Q_value1[s0][s1][a+4] += 1
                if done:
                    value = r
                    if r == -1:
                        Q_value1[s0][s1][a] -= 10#避免去已知不好的地方
                else:
                    value = r + gamma * max(Q_value1[s_0][s_1][:4])
                Q_value1[s0][s1][a] = (1 - alpha) * Q_value1[s0][s1][a] + alpha * value
                episode_reward += r
                s = s_
                eating = s[4]
                if done:
                    episode1 += 1
                   # env.render()
                  #  time.sleep(0.5)
                    break
                if episode1 >= 50 and len(visited1)>10:
                    for times in range(10*(len(visited1)-10)):
                        s1 = [random.randint(0, 5), random.randint(0, 5)]
                        while Model1[s1[0]][s1[1]][5] == 0:
                            s1 = [random.randint(0, 5), random.randint(0, 5)]
                        a =agent.choose_action(s, Q_value1, episode1,eating)
                        if Model1[s1[0]][s1[1]][a] == 0:
                            random.choice([opt for opt in [0, 1, 2, 3] if Model1[s1[0]][s1[1]][opt] == 1])
                        if a == 0:
                            s2 = [s1[0], s1[1] - 1]
                        elif a == 1:
                            s2 = [s1[0], s1[1] + 1]
                        elif a == 2:
                            s2 = [s1[0] + 1, s1[1]]
                        else:
                            s2 = [s1[0] - 1, s1[0]]
                        if s2[0] >= 0 and s2[0] < 6 and s2[1] >= 0 and s2[1] < 6:
                            r_new = Model1[s2[0]][s2[1]][4]
                            Q_value1[s1[0]][s1[1]][a] += alpha * (
                                        r_new + gamma * max(Q_value1[s2[0]][s2[1]][:4])
                                        - Q_value1[s1[0]][s1[1]][a])
        print('episode:', episode, 'episode1',episode1,'episode_reward:', episode_reward,'step',step)
        episode_list.append(episode)
        episode_rewards.append(episode_reward)
        step_list.append(step)


    plt.plot(episode_list, step_list, 'ob-')
    plt.title('Step each episode')
    plt.ylabel('Step')
    plt.xlabel('Episodes')
    plt.grid()
    plt.show()

    ### END CODE HERE ###

    print('\ntraining over\n')
