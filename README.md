### Quantum Gomoku with bot - README

---

#### **Introduction**
Quantum Gomoku is a novel take on the classic Gomoku (Five-in-a-Row) game. It combines traditional gameplay with principles of quantum mechanics to introduce new layers of uncertbotnty and strategy. This project also integrates a custom-built bot for playing agbotnst human opponents or other bot agents.


![image](https://github.com/user-attachments/assets/c5b2764d-b6a7-4dc3-9054-0ed6f67fd06e)



---

#### **Features**
1. **Classic Moves**: Play Gomoku with traditional rules.
2. **Quantum Moves**: Introduce quantum superposition by placing a single piece in two positions simultaneously.
3. **Quantum Collapsing**: Collapse quantum pieces to determine their final positions.
4. **bot Strategy**: The bot leverages minimax with alpha-beta pruning and custom heuristics for both classic and quantum moves.
5. **GUI Interface**: A fully interactive game board created using `Tkinter`.

---

#### **File Structure**
- **`run.py`**: Mbotn entry point for the game, sets up the GUI, and handles player interactions.
- **`bot.py`**: Contbotns bot logic, including minimax algorithm and evaluation functions.
- **`eval_fn.py`**: Implements custom evaluation functions for scoring game states.
- **`game.py`**: Core game logic for handling moves, quantum mechanics, and bot integration.
- **`board.py`**: Manages the board state and provides helper functions for move validation.
- **`piece.py`**: Defines constants and symbols for game pieces (classic and quantum).
- **`run_bot.py`**: A variant of the game that focuses on bot testing and execution.

---

#### **Installation**
Run the game:
   ```bash
   python run.py
   python run_bot.py
   ```

---
#### **Gameplay Instructions**
1. Launch the game using `run.py` or `run_bot.py` for bot game..
2. Use the mouse to click and place pieces:
   - **Classic Move**: Click on a grid cell to place a piece.
   - **Quantum Move**: Activate quantum mode using the "Quantum" button, then place two superposed pieces.
   - **Measure**: Activate measure mode using the "Measure" button and click on a quantum piece to collapse it.
3. The game alternates turns between two players or a player and the bot.
4. To restart the game, click the "Restart" button.
---

#### **Quantum Mechanics in Gameplay**
- **Quantum Superposition**: Pieces in superposition exist simultaneously in two locations.
- **Quantum Entanglement**: Opposite quantum pieces at the same position create a "grey" quantum piece that cannot overlap further.
- **Measurement**: Measuring a quantum piece collapses its state, finalizing its position.

---

#### **bot Strategy**
Huge thanks to https://github.com/linhusp/gomoku-alphabeta for inspiration about bot stucture
The bot uses a combination of:
- **Minimax Algorithm**: Evaluates possible moves and selects the optimal path.
- **Alpha-Beta Pruning**: Reduces computation by eliminating non-promising moves.
- **Custom Evaluation Function**: Scores board states based on potential winning opportunities, threats, and quantum superpositions.

---

#### **Future Work**
- Expand quantum mechanics with more advanced entanglement rules like negative entanglement.
- Enable multiplayer support over a network.
- Enhance the bot with machine learning techniques.
