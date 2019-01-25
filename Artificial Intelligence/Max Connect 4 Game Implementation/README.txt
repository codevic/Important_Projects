Code Structure :
Classes : maxconnect4, AiPlayer, GameBoard
 
----------------------------------------------------------------------------
class maxconnect4 :
methods : main(), InteractivePlayComputerMove(), OneMovePlayComputerMove(output), HumanMove(), printResult(), printDetails(), isValidPlay(playColumn), exit_function(value).


HumanMove() -> this function takes input from user and makes the next move for human player.
InteractivePlayComputerMove() -> this function is called when the computer has to make a move for an interactive mode game.
OneMovePlayComputerMove() -> this function is called when the computer has to make a move for a one-move mode game.
printDetails() -> this function prints the board's current state and the current score. 
printResult() -> this function prints the final score and declares winner or tie.
isValidPlay(playColumn) -> this function checks if the input from the user is a valid column.

----------------------------------------------------------------------------
class AiPlayer :
methods : findBestPlay(), Min_Utility(), Max_Utility()

findBestPlay() -> this function makes the decision to make a move for the computer using the min and max value from the below given two functions
Calculate_Min_Utility() -> this function calculates the min value.
Calculate_Min_Utility() -> this function calculates the max value.

-----------------------------------------------------------------------------
class GameBoard :
methods : getScore(), getCurrentTurn(), getGameBoard(), printGameBoard(), isBoardFull(), getPlayer(), setPlayer()

getScore() -> this function takes the current score and send it to printBoardAndScore() to print score.
getCurrentTurn() -> this function traces the current turn.
getGameBoard() -> this function takes the current gameboard state and pass it to printGameBoard() function.
printGameBoard() -> this function prints the current board state.
isBoardFull() -> this function determines if the board is full.
getPlayer() -> this function gets the player values.
setPlayer() -> this function sets the player values.

-----------------------------------------------------------------------------

-> Evaluation function :
       AiPlayer.findBestPlay():
        This method uses the minmax algorithm along with alpha beta pruning and depth limited search to make the best move the computer can make to win or tie the game.
        It takes current game board state as input.
        For each valid column inputted, it calls the Min_Utility() or Max_Utility() depending on the player.
        Max_Utility()  and Min_Utility(): takes 4 parameters gameboard, depth, alpha and beta. They run until depth becomes 0. They use alpha beta pruning and each time reduces depth by 1.
        The findBestPlay() returns the optimal column number decided by the function.

------------------------------------------------------------------------------
How to run Code :
Compile using :
        javac -classpath . maxconnect4.java

Execute using :
        (for interactive mode) :
        java maxconnect4 interactive [input_file] [computer-next/human-next] [depth]  
        for example: java maxconnect4 interactive input.txt computer-next 8

        (for one-move mode) :
        time java maxconnect4 one-move [input_file] [output_file] [depth]  
        for example: java maxconnect4 one-move input1.txt output.txt 8

Command to retrieve execution time:
        time java maxconnect4 one-move [input_file] [output_file] [depth]  
        for example: java maxconnect4 one-move input1.txt output.txt 8

-------------------------------------------------------------------------------
 The depth and execution time of user results are as below:

         -------------------------------------
        || Depth Level || Execution Time(user) ||
          -------------------------------------
        ||     1       ||        0m0.047s      ||
        ||     2       ||        0m0.097s      ||
        ||     3       ||        0m0.113s      ||
        ||     4       ||        0m0.118s      ||
        ||     5       ||        0m0.136s      ||
        ||     6       ||        0m0.140s      ||
        ||     7       ||        0m0.426s      ||
        ||     8       ||        0m0.647s      ||
        ||     9       ||        0m1.017s      ||
        ||     10      ||        0m2.107s      ||
        ||     11      ||        0m5.241s      ||
        ||     12      ||        1m30.082s     ||
        ||     13      ||        5m51.101s     ||
        ||     14      ||        7m4.610s      ||
         -------------------------------------
-------------------------------------------------------------------------------