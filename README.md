# 🌸 Flower Puzzle

A logic game developed in Python using Tkinter. The goal is to place **one flower per row, column, and region**, following rules of **uniqueness** (per row / column) and **non-adjacency**.

Feel free to download the code and play with it! Be mindful that this game is not perfect. I'm still figuring out how to grant **uniqueness** of the entire solution. Suggestions are more than appreciated.

This game was built thinking of a LinkedIn game I'm a little obsessed about xD One session per day just wasn't enough.

---

## 📦 Features

* ✅ 7x7 grid randomly generated
* 🎯 Goal: place 7 flowers (🌸) following the rules
* 🧩 Dynamically generated connected color regions
* 🚫 Flowers cannot touch each other (not even diagonally)
* 🤖 **Hint** button to reveal a correct flower
* 🔁 Buttons for **Check**, **Clear**, and **New Puzzle**

---

## 🕹️ Game Rules

1. Each **row**, **column**, and **colored region** must contain **exactly one flower** (🌸).
2. Flowers **cannot touch each other**, not even diagonally.
3. Click a cell to toggle between: empty → ❌ → 🌸 → empty.
4. Use the buttons to check the solution, clear the grid, or get a hint.

---

## 🚀 Running the Game

### Requirements

* Python 3.x

### Start

Save the script as `.py` and run it with:

```bash
python flower_puzzle.py
```

---

## 🧠 Code Structure

* `generate_flower_solution()`: generates a valid flower arrangement
* `create_connected_regions()`: builds connected regions around flowers
* `redraw_canvas()`: draws the grid and updates symbols
* `check_solution()`: checks whether the solution meets the constraints

---

## 📷 Screenshot

WIP

---

## ✍️ Author

Created with passion by **Irene de Cesare**.

---

## 🙏 Special Thanks
Special thanks to ChatGPT (by OpenAI) for providing design suggestions during development and writing this README xD.


