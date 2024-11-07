
from bstack import BoundedStack
from bqueue import BoundedQueue
import os 

# ANSI escape sequences for color and formatting in terminal output
ANSI = {
        "RED": "\033[31m",
        "GREEN": "\033[32m",
        "HRED": "\033[41m",
        "HGREEN": "\033[42m",
        "HYELLOW": "\033[43m",
        "HBLUE": "\033[44m",
        "HMAGENTA": "\033[45m",
        "HORANGE": "\033[48;5;208m",  
        "UNDERLINE": "\033[4m",
        "RESET": "\033[0m",
        "CLEARLINE": "\033[0K"
    }

class ChemicalFlask(BoundedStack):
    """A class representing a chemical flask, inheriting from BoundedStack."""
    
    def __init__(self, limit=4):
        """Initialize a ChemicalFlask object with a specified limit."""
        super().__init__(limit)
    
    def is_top_sealed(self):
        """Flask is considered sealed if it has exactly three substances and they are all the same."""
        return self.size() == 3 and len(set(self.stack_from_string())) == 1
    
    def stack_from_string(self):
        """Creates a list copy of the stack from the str function of BoundedStack"""
        stack_str = str(self)
        stack_list = stack_str.split()
        return stack_list
        
        
class GameImplementation:
    
    def __init__(self, filepath):
        """Initialize the game by loading chemicals from a file into flasks."""
        self.flasks = []  # List to hold all the flasks
        self.chem_queue = BoundedQueue(4)  # Queue to temporarily hold chemicals
        self.load_chemicals(filepath)  # Load chemicals from the given file

    
    def load_chemicals(self, filepath):
        """
        Load chemicals from the file and distribute them into the flasks.
        Args: 
            filepath (str): The path to the file containing chemical information.
        Returns: 
            None
        """
        # Open the file for reading
        with open(filepath, "r") as file:
            # Read the first line containing information about the number of flasks and their limit
            d1 = file.readline().strip().split()
            num_flasks, _ = int(d1[0]),int(d1[1])
            # Create flasks based on the number specified in the file
            self.flasks = [ChemicalFlask(4) for _ in range(num_flasks)]
            # Iterate through each line in the file
            for line in file:
                stripped_line = line.strip()
                # If the line starts with a number, it represents the number of chemicals to add to a flask
                if stripped_line[0].isnumeric():  
                    d2 = stripped_line.split('F')
                    qnty, flask_indx = int(d2[0]),int(d2[1])
                    # Distribute chemicals from the queue to the specified flask
                    for _ in range(qnty):
                        if not self.chem_queue.isEmpty():
                            self.flasks[flask_indx - 1].push(self.chem_queue.dequeue())
                # If the line does not start with a number, it represents a single chemical to add to the queue
                else:
                    if not self.chem_queue.isFull():
                        self.chem_queue.enqueue(stripped_line)
        
    def pour_chemical(self, source, destination):
        """
        Pour chemical from one flask to another.

        Args:
            source (int): The index of the source flask.
            destination (int): The index of the destination flask.

        Returns:
            bool: True if the pour operation was successful, False otherwise.
        """
        # Retrieve the source and destination flasks based on their indices
        source_flask = self.flasks[source - 1]
        destination_flask = self.flasks[destination - 1]
        
        # Check if source flask is empty or sealed
        if source_flask.isEmpty() or source_flask.is_top_sealed():
            return False
        
        # Check if destination flask is full or sealed     
        if destination_flask.isFull() or destination_flask.is_top_sealed():
            return False
        
        # Pour chemical from source flask to destination flask
        chemical = source_flask.pop()
        destination_flask.push(chemical)
        return True
    
    
    def get_and_validate_input(self):
        """
        Get user input for selecting source and destination flasks and validate the input.

        Returns:
            Union[bool, Tuple[int, int]]: 
            - False if the user chooses to exit the game.
            - Tuple[int, int] containing the validated source and destination flask indices.
        """
        # Initialize boolean flags and variables
        valid_source_input = False # Flag to track if the input for the source flask is valid
        valid_destination_input = False # Flag to track if the input for the destination flask is valid
        source = destination = None  # Initialize source and destination indexes
        
        # Prompt user to select source and destination flasks
        print_location(3, 0, "Select source flask: ")
        print_location(4, 0, "Select destination flask: ")
        print_location(5,0 , ANSI['CLEARLINE'])
        
        # Main input loop
        while True:
            if not valid_source_input:
                # Step 1: Take input for the source flask
                move_cursor(3, len("Select source flask: ") + 1)
                print(ANSI['CLEARLINE'],end='')
                source_str = input().strip()
                if source_str.lower() == "exit":
                    return False # Exit if the user chooses to exit the game

                # Validate source input
                move_cursor(5,0)
                print(ANSI['CLEARLINE'],end='')
                if source_str.isdigit() and 1 <= int(source_str) <= len(self.flasks):
                    if self.flasks[int(source_str)-1].is_top_sealed() or self.flasks[int(source_str)-1].isEmpty():
                        print("Cannot pour from that flask. Try again.",end='')
                    else:
                        source = int(source_str)
                        valid_source_input = True
                else:
                    print("Invalid input. Try again.", end='')
                
            if not valid_destination_input and valid_source_input:
                # Step 2: Take input for the destination flask
                move_cursor(4, len("Select destination flask: ") + 1)
                print(ANSI['CLEARLINE'],end='')
                destination_str = input().strip()
                if destination_str.lower() == 'exit':
                    return False # Exit if the user chooses to exit

                # Validate destination input
                move_cursor(5,0)
                print(ANSI['CLEARLINE'],end='')
                if destination_str.isdigit() and 1 <= int(destination_str) <= len(self.flasks):
                    if self.flasks[int(destination_str)-1].is_top_sealed() or self.flasks[int(destination_str)-1].isFull():
                        print("Cannot pour into that flask. Try again.")
                    else:
                        destination = int(destination_str)
                        valid_destination_input = True
                else:
                    print("Invalid input. Try again.", end='')
                
                # Check if both source and destination inputs are valid
                if valid_source_input and valid_destination_input:
                    # Check if both source and destination inputs are the same
                    if source == destination:
                        move_cursor(5,0)
                        print(ANSI['CLEARLINE'],end='')
                        valid_destination_input = False
                        print_location(5,0,"Cannot pour into the same flask. Try again.")
                        move_cursor(4, len("Select destination flask: ") + 1)
                        print(ANSI['CLEARLINE'],end='')
                    else:
                        return source, destination # Return the validated source and destination indices
        
            
    def print_row_level(self, flasks):
        color_map = {
        'AA': ANSI['HRED'],    # Background color for Chemical A
        'BB': ANSI['HBLUE'],   # Background color for Chemical B
        'CC': ANSI['HGREEN'],  # Background color for Chemical C
        'DD': ANSI['HORANGE'], # Background color for Chemical D
        'EE': ANSI['HYELLOW'], # Background color for Chemical E
        'FF': ANSI['HMAGENTA'] # Background color for Chemical F
        }
        for level in range(4, 0, -1):
            for flask in flasks:
                # Determine the content to be printed based on the current level and flask state
                content = "+--+" if level == 4 and flask.is_top_sealed() else "|  |" if level > flask.size() else f"|{color_map[flask.stack_from_string()[level - 1] if not flask.is_top_sealed() else flask.stack_from_string()[0]]}{flask.stack_from_string()[level - 1] if not flask.is_top_sealed() else flask.stack_from_string()[0]}{ANSI['RESET']}|"
                print(content, end="  ") 
            print() # Move to the next line
        print(' '.join(["+--+ " for _ in flasks])) # Base for each flask

    
    def print_flask_numbers(self, start, end, source=None, destination=None):
        """
        Print flask numbers with highlighting for source and destination.

        Args:
            start (int): The starting flask number (inclusive).
            end (int): The ending flask number (inclusive).
            source (int, optional): The source flask number to highlight (default: None).
            destination (int, optional): The destination flask number to highlight (default: None).

        Returns:
            None
        """
        # Iterate through flask numbers from start to end
        for flask_number in range(start+1, end+1):
            # Highlight the source flask number in red
            if flask_number == source:
                color = ANSI['RED']  # Red text for the source flask number
            # Highlight the destination flask number in green
            elif flask_number == destination:
                color = ANSI['GREEN']  # Green text for the destination flask number
            # Reset color for other flask numbers
            else:
                color = ANSI['RESET']
            # Print flask number with color formatting
            print(f"  {color}{flask_number}{ANSI['RESET']} ", end="  ")
        # Move to the next line after printing all flask numbers
        print("\n")

    def show_flasks(self, source=None, destination=None):
        """
        Display the flasks with optional highlighting for source and destination.

        Args:
            source (int, optional): The source flask number to highlight (default: None).
            destination (int, optional): The destination flask number to highlight (default: None).

        Returns:
            None
        """
        # Calculate the number of full rows
        num_full_rows = len(self.flasks) // 4
        # Calculate the number of remaining flasks
        remaining_flasks_count = len(self.flasks) % 4
        
        move_cursor(6,0) # Move the cursor to the specified position (6,0)
        
        # Iterate over full rows
        for row_index in range(num_full_rows):
            start_index = row_index * 4
            end_index = start_index + 4
            # Print the flask levels for the current row
            self.print_row_level(self.flasks[start_index:end_index])
            # Print the flask numbers for the current row with optional highlighting
            self.print_flask_numbers(start_index, end_index, source, destination)
        
        # Print remaining flasks if any
        if remaining_flasks_count:
            start_index = len(self.flasks) - remaining_flasks_count
            end_index = len(self.flasks)
            # Print the flask levels for the remaining flasks
            self.print_row_level(self.flasks[start_index:end_index])
            # Print the flask numbers for the remaining flasks with optional highlighting
            self.print_flask_numbers(start_index,end_index, source, destination)
       

    def check_all_sealed(self):
        """
        Check if all flasks are sealed at the top and not empty.

        Returns:
            bool: True if all flasks are sealed and not empty, False otherwise.
        """
        # Iterate over each flask in the list of flasks
        for flask in self.flasks:
            # Check if the top of the flask is sealed and the flask is not empty
            if not flask.is_top_sealed() and not flask.isEmpty():
                # If any flask is not sealed at the top and not empty, return False
                return False
        # If all flasks are sealed at the top and not empty, return True
        return True
    
    def game_start(self):
        """
        Starts the magical flask game.

        Initializes the game and runs the main game loop until the game is won or ended by the user.
 
        Args:
            self (object): The instance of the FlaskGame class.

        Returns:
            None
        """
        game_active = True # Initialize game variables
        clear_screen() # Clear the screen
        print_location(1, 0, "Magical Flask Game") # Print game title 
        self.show_flasks() # Show initial state of flasks
        
        # Main game loop
        while game_active:
            # Get user action and validate input
            user_action = self.get_and_validate_input()
            
            # Check if user ended the game
            if user_action is False:
                move_cursor(5,0)
                print(ANSI['CLEARLINE'],end='')
                print("Game ended by user.")
                game_active = False
            # If user action is valid, proceed with pouring chemical
            elif user_action is not None:
                # Extract source and destination flasks from user action
                source, destination = user_action
                # Pour chemical from source to destination flask
                action_success = self.pour_chemical(source, destination)
        
                clear_screen() # Clear the screen
                print_location(1, 0, "Magical Flask Game") # Print game title
                self.show_flasks() # Show updated state of flasks
            
            # Check if all flasks are sealed and the game is won
            if self.check_all_sealed():
                print("You win!")
                game_active = False
        
      
def clear_screen():
    """
    Clears the Screen
    Args:
        N/A
    Returns:
        None
    """
    os.system("cls") if os.name == "nt" else os.system("clear") #cls for windows (when name == nt) and clear for Mac and Linux
    
def move_cursor(x, y):
    """
    Moves the cursor to the provided x and y coordinates
    Args:
        x: int
        y: int
    Returns:
        None
    """
    print(f"\033[{x};{y}H", end = "")

def print_location(x, y, text):
    """
    Prints the provided text at the given x and y. 
    Args:
        x: int
        y: int
        text: str
    Returns:
        None
    """
    print(f"\033[{x};{y}H{text}")


def main():
    
    chemical_game = GameImplementation("chemicals.txt")  
    chemical_game.game_start()  

if __name__ == "__main__":
    main() 
    

    



    
