/**
 * @author kavya
 */

import java.util.Scanner;

/**
 * This class controls the game play for the Max Connect-Four game. 
 * To compile the program, use the following command from the maxConnectFour directory:
 * javac *.java
 */

public class maxconnect4
{

	private static GameBoard currentGame;
	private static AiPlayer calculon;
	private static Scanner inStream;

	public static void main(String[] args) 
	{
		// check for the correct number of arguments
		if( args.length != 4 ) 
		{
			System.out.println("Four command-line arguments are needed:\n"
					+ "Usage: java [program name] interactive [input_file] [computer-next / human-next] [depth]\n"
					+ " or:  java [program name] one-move [input_file] [output_file] [depth]\n");

			exit_function( 0 );
		}

		// parse the input arguments
		String game_mode = args[0].toString();				// the game mode
		String input = args[1].toString();					// the input game file
		int depthLevel = Integer.parseInt( args[3] );  		// the depth level of the ai search

		// create and initialize the game board
		currentGame = new GameBoard( input );

		// create the Ai Player
		calculon = new AiPlayer(depthLevel, currentGame);

		if( game_mode.equalsIgnoreCase( "interactive" ) ) 
		{
			currentGame.setGameMode("interactive");
			if (args[2].toString().equalsIgnoreCase("computer-next") || args[2].toString().equalsIgnoreCase("C")) {
				// if it is computer next, make the computer make a move
				currentGame.setFirstMove("computer");
				InteractivePlayComputerMove();
			} else if (args[2].toString().equalsIgnoreCase("human-next") || args[2].toString().equalsIgnoreCase("H")){
				currentGame.setFirstMove("human");
				HumanMove();
			} else {
				System.out.println("\n" + "value for 'next turn' doesn't recognized.  \n try again. \n");
				exit_function(0);
			}

			if (currentGame.isBoardFull()) {
				System.out.println("\nI can't play.\nThe Board is Full\n\nGame Over.");
				exit_function(0);
			}
		} 

		else if(game_mode.equalsIgnoreCase("one-move")) 
		{
			// /////////// one-move mode ///////////
			currentGame.setGameMode("one-move");
			String outputFileName = args[2].toString(); // the output game file
			OneMovePlayComputerMove(outputFileName);
		}
		else {
			System.out.println( "\n" + game_mode + " is an unrecognized game mode \n try again. \n" );
			return;
		}
	} // end of main()

	private static void InteractivePlayComputerMove() {
		// TODO Auto-generated method stub
		printDetails();

		System.out.println("\n Computer's turn:\n");

		int playColumn = 99; // the players choice of column to play

		// AI play - random play
		playColumn = calculon.findBestPlay(currentGame);

		if (playColumn == 99) {
			System.out.println("\nI can't play.\nThe Board is Full\n\nGame Over.");
			return;
		}

		// play the piece
		currentGame.playPiece(playColumn);

		System.out.println("move: " + currentGame.getPieceCount() + " , Player: Computer , Column: " + (playColumn + 1));

		currentGame.printGameBoardToFile("computer.txt");

		if (currentGame.isBoardFull()) {
			printDetails();
			printResult();
		} else {
			HumanMove();
		}
	}

	private static void OneMovePlayComputerMove(String output) {
		// TODO Auto-generated method stub

		// variables to keep up with the game
		int playColumn = 99; // the players choice of column to play
		
		System.out.print("\nMaxConnect-4 game\n");
		System.out.print("game state before move:\n");

		//print the current game board
		currentGame.printGameBoard();
		// print the current scores
		System.out.println( "Score: Player 1 = " + currentGame.getScore( 1 ) +
				", Player2 = " + currentGame.getScore( 2 ) + "\n " );

		// Check if board is full!
		if (currentGame.isBoardFull()) {
			System.out.println("\nThe Board is Full. I canont play!!\nGame Over.");
			return;
		}
		// ****************** this chunk of code makes the computer play
		int current_player = currentGame.getCurrentTurn();
		playColumn = calculon.findBestPlay(currentGame);

		if(playColumn == 99) {
			System.out.println("\nThe Board is Full. I canont play!!\nGame Over.");
			return;
		}

		currentGame.playPiece(playColumn);

		System.out.println("move " + currentGame.getPieceCount() 
		+ ": Player " + current_player
		+ ", column " + playColumn);
		System.out.print("game state after move:\n");

		// dispaly the current game board state
		currentGame.printGameBoard();

		// display the current scores
		System.out.println( "Score: Player 1 = " + currentGame.getScore( 1 ) +
				", Player2 = " + currentGame.getScore( 2 ) + "\n " );

		currentGame.printGameBoardToFile( output );

	}

	private static void HumanMove() {
		// TODO Auto-generated method stub
		printDetails();
		System.out.println("\n Human's turn:\nKindly play your move here(1-7):");

		inStream = new Scanner(System.in);

		int playColumn = 99;

		do {
			playColumn = inStream.nextInt();
		} while (!isValidPlay(playColumn));

		// play the piece
		currentGame.playPiece(playColumn - 1);

		System.out.println("move: " + currentGame.getPieceCount() + " , Player: Human , Column: " + playColumn);

		currentGame.printGameBoardToFile("human.txt");

		if (currentGame.isBoardFull()) {
			printDetails();
			printResult();
		} else {
			InteractivePlayComputerMove();
		}
	}

	private static void printResult() {
		// TODO Auto-generated method stub
		int h = 0 ,c = 0;
		String player = currentGame.getPlayer();
		if(player.equals("human"))
		{
			h = 1;
			c = 2;
		}
		else {
			h = 2;
			c = 1;
		}
		int humanScore = currentGame.getScore(h);
		int computerScore = currentGame.getScore(c);
	
		System.out.println("\n Result:");
		if(humanScore > computerScore){
			System.out.println("\n Congratulations!! You won this game."); 
		} else if (humanScore < computerScore) {
			System.out.println("\n You lost!! Good luck next time.");
		} else {
			System.out.println("\n Game is tie !!");
		}
	}

	private static void printDetails() {
		// TODO Auto-generated method stub
		System.out.print("Game state :\n");

		// print the current game board
		currentGame.printGameBoard();

		// print the current scores
		System.out.println("Score: Player-1 = " + currentGame.getScore(1) + ", Player-2 = " + currentGame.getScore(2)
		+ "\n ");
	}

	private static boolean isValidPlay(int playColumn) {
		if (currentGame.isValidPlay(playColumn - 1)) {
			return true;
		}
		System.out.println("Opps!!...Invalid column , Kindly enter column value between 1 to 7.");
		return false;
	}

	/**
	 * This method is used when to exit the program prematurly.
	 * @param value an integer that is returned to the system when the program exits.
	 */
	private static void exit_function( int value )
	{
		System.out.println("exiting from MaxConnectFour.java!\n\n");
		System.exit( value );
	}
} // end of class connectFour