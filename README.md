# RL_TicTacToe

Authors: Jewin CHENG, Mathusan SELVAKUMAR

## Abstract
This repository is for the course Communication in Paris-Saclay university Master 1 ISD. The goal for this repository is to be introduced in reinforcement learning through a little game.


## Roadmap

### **Phase 1: Basic Game Implementation (1-2 days)**  
✅ **Goal:** Create a functional Tic-Tac-Toe game with a simple command-line interface (CLI).  

🔹 **Tasks:**  
- [X] Define the 3x3 board as a NumPy array or list.  
- [ ] Implement functions to:  
  - [X] Display the board  
  - [X] Check for a win or draw condition  
  - [X] Handle player moves  
- [X] Add basic user interaction (human vs. human mode).  

🔹 **Milestone:** A fully functional CLI Tic-Tac-Toe game.  

---

### **Phase 2: Implementing Random and Rule-Based Agents (2-3 days)**  
✅ **Goal:** Create baseline agents to play against.  

🔹 **Tasks:**  
- [ ] Implement a **random agent** that selects moves randomly.  
- [ ] Implement a **rule-based agent** using the Minimax algorithm (optional, for benchmarking).  
- [ ] Allow human vs. AI and AI vs. AI matches.  

🔹 **Milestone:** Basic AI players that can play the game.  

### Main objective :
- [ ] Creating slides presentation

---

## Bonus

### **Phase 3: Environment Setup for Reinforcement Learning (3-4 days)**  
✅ **Goal:** Set up Tic-Tac-Toe as an RL environment.  

🔹 **Tasks:**  
- [ ] Define state representation (e.g., board as a flattened array).  
- [ ] Define actions (valid moves).  
- [ ] Define rewards:  
  - +1 for a win, -1 for a loss, 0 for a draw.  
- [ ] Implement an **environment class** (like in OpenAI Gym).  

🔹 **Milestone:** A well-structured environment that supports RL training.  

---

### **Phase 4: Implementing Reinforcement Learning Agent (5-7 days)**  
✅ **Goal:** Train an RL agent using Q-learning or Deep Q-Networks (DQN).  

🔹 **Tasks:**  
- **Tabular Q-learning approach (basic):**  
  - [ ] Initialize a Q-table mapping state-action pairs to values.  
  - [ ] Implement the **ε-greedy policy** for exploration/exploitation.  
  - [ ] Train the agent via episodes.  

- **Deep RL approach (optional, advanced):**  
  - [ ] Use a **Neural Network** instead of a Q-table (DQN).  
  - [ ] Implement experience replay and target networks for stability.  

🔹 **Milestone:** A trained RL agent that improves over time.  

---

### **Phase 5: Evaluating & Optimizing the RL Agent (3-5 days)**  
✅ **Goal:** Assess agent performance and fine-tune training.  

🔹 **Tasks:**  
- [ ] Play RL agent vs. random agent → Measure win rate.  
- [ ] Play RL agent vs. Minimax → Evaluate competitiveness.  
- [ ] Fine-tune hyperparameters (learning rate, discount factor, exploration rate).  
- [ ] Implement model saving/loading for trained agents.  

🔹 **Milestone:** An RL agent that consistently beats random players and competes well against Minimax.  

---

### **Phase 6: Finalization & Deployment (2-4 days)**  
✅ **Goal:** Wrap up the project and showcase results.  

🔹 **Tasks:**  
- [ ] Create a **Graphical User Interface (GUI)** (e.g., Tkinter, Pygame) OR a web app.  
- [ ] Provide an option for users to play against the RL agent.  

🔹 **Milestone:** A polished, user-friendly Tic-Tac-Toe AI.  