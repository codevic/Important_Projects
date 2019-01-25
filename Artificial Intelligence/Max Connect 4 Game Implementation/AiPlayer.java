/**
 * @author kavya
 *
 * This is the AiPlayer class.  It simulates a minimax player for the max
 * connect four game. 
 */

public class AiPlayer 
{
	public int depth;
	public GameBoard gameBoard;

	/**
	 * The constructor instantiates an AiPlayer object and it's attributes.
	 */
	public AiPlayer(int depth, GameBoard currGameBoard) {
		this.depth = depth;
		this.gameBoard = currGameBoard;
	}

	/**
	 * This method plays a piece on the board. It employs the MINMAX algorithm/
	 * 
	 * @param currentGame The GameBoard object that is currently being used to
	 * play the game.
	 * @return an integer indicating which column the AiPlayer would like
	 * to play in.
	 */
	public int findBestPlay( GameBoard currentGame ) 
	{
		int playChoice = 0;
		int value = 0, utility = 0;
		GameBoard nextGameBoard;
		if( currentGame.getCurrentTurn() == 1) {
			value = Integer.MAX_VALUE;
			for(int i = 0; i < 7; i++) {
				if(currentGame.isValidPlay(i)) {
					nextGameBoard = new GameBoard(currentGame.getGameBoard());
					nextGameBoard.playPiece(i);
					utility = Max_Utility(nextGameBoard, depth, Integer.MIN_VALUE, Integer.MAX_VALUE);
					if(value > utility) {
						playChoice = i;
						value = utility;
					}
				}
			}
		}
		else {
			value = Integer.MIN_VALUE;
			for(int i = 0; i < 7; i++) {
				if(currentGame.isValidPlay(i)) {
					nextGameBoard = new GameBoard(currentGame.getGameBoard());
					nextGameBoard.playPiece(i);
					utility = Min_Utility(nextGameBoard, depth, Integer.MIN_VALUE, Integer.MAX_VALUE);
					if(value < utility) {
						playChoice = i;
						value = utility;
					}
				}
			}
		}
		return playChoice;
	}

	/**
	 * This method calculates MIN value.
	 */
	private int Min_Utility(GameBoard gameBoard, int depth, int alpha, int beta) {
		// TODO Auto-generated method stub
		if(!gameBoard.isBoardFull() && depth > 0) {
			int value = Integer.MAX_VALUE;
			int utility = 0;
			GameBoard nextGameBoard;
			for(int i = 0; i < 7; i++) {
				if(gameBoard.isValidPlay(i)) {
					nextGameBoard = new GameBoard(gameBoard.getGameBoard());
					nextGameBoard.playPiece(i);
					utility = Max_Utility(nextGameBoard, depth-1, alpha, beta);
					value = Math.max(value, utility);
					if (value <= alpha)
						return value;
					beta = Math.max(value, beta);
				}
			}
			return value;
		}
		else {
			// terminal state
			int value = gameBoard.getScore(2) - gameBoard.getScore(1);
			return value;
		}		
	}

	/**
	 * This method calculates MAX value.
	 */
	private int Max_Utility(GameBoard gameBoard, int depth, int alpha, int beta) {
		// TODO Auto-generated method stub
		if(!gameBoard.isBoardFull() && depth > 0) {
			int value = Integer.MIN_VALUE;
			int utility = 0;
			GameBoard nextGameBoard;
			for(int i = 0; i < 7; i++) {
				if(gameBoard.isValidPlay(i)) {
					nextGameBoard = new GameBoard(gameBoard.getGameBoard());
					nextGameBoard.playPiece(i);
					utility = Min_Utility(nextGameBoard, depth-1, alpha, beta);
					value = Math.max(value, utility);
					if (value >= beta)
						return value;
					alpha = Math.max(value, alpha);
				}
			}
			return value;
		}
		else {
			// terminal state
			int value = gameBoard.getScore(2) - gameBoard.getScore(1);
			return value;
		}		
	}
}
