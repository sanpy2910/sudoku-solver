# Sudoku Solver Using Machine Learning and Selenium

This project is a Sudoku solver that utilizes machine learning techniques and Selenium to solve Sudoku puzzles in various modes. The solver employs different approaches tailored to each mode, ensuring an efficient and versatile solution.

## Features

- **Manual Mode**: Allows the user to solve a standard Sudoku puzzle by clicking the "Solve" button.
- **Image Mode**: Takes an image as input, overlays the solution on the image, and displays the result.
- **Website Mode**: Opens a website and solves the Sudoku challenge present on that website, overlaying the solution.
- **Video Mode**: Captures live video, solves the Sudoku puzzle within the video frame, and overlays the solution in real-time.

## Prerequisites

- Python 3.x
- Pip (Python package installer)

## Installation

1. Clone the repository:git clone https://github.com/santoshkanumuri/sudoku-solver.git
2. Navigate to the project directory: cd sudoku-solver
3. Install the required Python packages: pip install -r requirements.txt
## Usage

1. Run the main UI script:python main.py
2. Select the desired mode from the UI options.
3. Follow the prompts and provide the required inputs based on the selected mode.

## Machine Learning Approach

This Sudoku solver utilizes a Convolutional Neural Network (CNN) to recognize and solve Sudoku puzzles. The CNN is trained on a large dataset of Sudoku puzzles and their corresponding solutions, enabling it to learn the patterns and relationships between the puzzle inputs and their solutions.

The CNN architecture consists of multiple convolutional layers, pooling layers, and dense layers, which work together to extract features from the input puzzles and map them to the corresponding solutions. The trained model can then take new Sudoku puzzles as input and predict their solutions with high accuracy.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.
