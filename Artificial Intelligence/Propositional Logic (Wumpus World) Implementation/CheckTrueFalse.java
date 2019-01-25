import java.io.*;
import java.util.*;
import java.util.Map.Entry;
/**
 * @author kavya
 *
 */
public class CheckTrueFalse {

	static HashSet<String> listOfSymbols = new HashSet<String>();
	/**
	 * @param args
	 */
	public static void main(String[] args) {

		if( args.length != 3){
			//takes three arguments
			System.out.println("Usage: " + args[0] +  " [wumpus-rules-file] [additional-knowledge-file] [input_file]\n");
			exit_function(0);
		}
		//create some buffered IO streams
		String buffer;
		BufferedReader inputStream;
		BufferedWriter outputStream;
		//create the knowledge base and the statement
		LogicalExpression knowledge_base = new LogicalExpression();
		LogicalExpression statement1 = new LogicalExpression();
		LogicalExpression statement2 = new LogicalExpression();
		TTEntails ttEntails = new TTEntails();
		TTEntails.Model model = ttEntails.new Model();

		//open the wumpus_rules.txt
		try {
			inputStream = new BufferedReader( new FileReader( args[0] ) );
			//load the wumpus rules
			System.out.println("\nloading the wumpus rules...");
			knowledge_base.setConnective("and");
			while(  ( buffer = inputStream.readLine() ) != null ) 
			{
				if( !(buffer.startsWith("#") || (buffer.equals( "" )) )) 
				{
					//the line is not a comment
					LogicalExpression subExpression = readExpression( buffer );
					knowledge_base.setSubexpression( subExpression );
				}
			}		
			//close the input file
			inputStream.close();
		} catch(Exception e) 
		{
			System.out.println("failed to open " + args[0] );
			e.printStackTrace();
			exit_function(0);
		}
		//end reading wumpus rules
		//read the additional knowledge file
		try {
			inputStream = new BufferedReader( new FileReader( args[1] ) );
			//load the additional knowledge
			System.out.println("loading the additional knowledge...");
			// the connective for knowledge_base is already set.  no need to set it again.
			// i might want the LogicalExpression.setConnective() method to check for that
			//knowledge_base.setConnective("and");
			while(  ( buffer = inputStream.readLine() ) != null) 
			{
				if( !(buffer.startsWith("#") || (buffer.equals("") ))) 
				{
					String temp_buffer = buffer;
					if(temp_buffer.contains("not")) {
						String[] split_temp = temp_buffer.split(" ");
						split_temp[1] = split_temp[1].substring(0, split_temp[1].length()-1);
						model.hashMap.put(split_temp[1], false);
					}
					else {
						temp_buffer = temp_buffer.trim();
						model.hashMap.put(temp_buffer, true);
					}
					LogicalExpression subExpression = readExpression( buffer );
					knowledge_base.setSubexpression( subExpression );
				}
			}
			//close the input file
			inputStream.close();
		} catch(Exception e) {
			System.out.println("failed to open " + args[1] );
			e.printStackTrace();
			exit_function(0);
		}
		//end reading additional knowledge
		// check for a valid knowledge_base
		if( !valid_expression( knowledge_base ) ) {
			System.out.println("invalid knowledge base");
			exit_function(0);
		}
		// print the knowledge_base
		//knowledge_base.print_expression("\n");

		String alpha1 = "", alpha2 = "";
		// read the statement file
		try {
			inputStream = new BufferedReader( new FileReader( args[2] ) );
			System.out.println("Loading the statement file...");
			getSymbols(knowledge_base);
			Set<String> uniqueSetSymbol = listOfSymbols;
			//buffer = inputStream.readLine();
			// actually read the statement file
			// assuming that the statement file is only one line long
			while( ( buffer = inputStream.readLine() ) != null ) {
				if( !buffer.startsWith("#") ) {
					if(buffer.contains("not")) {
						alpha1 = buffer;
						String[] split_buffer = buffer.split(" ");
						alpha2 = split_buffer[1].substring(split_buffer[1].length() - 1);
					}
					else {
						alpha1 = buffer;
						alpha2 = "(not " + buffer + ")";
					}
					//the line is not a comment
					statement1 = readExpression( alpha1 );
					statement2 = readExpression( alpha2 );
					if (valid_expression(statement1)&& !isValidInput(alpha1, uniqueSetSymbol)) {
						System.out.println("invalid statement");
						return;
					}
					break;
				} 
			}
			//close the input file
			inputStream.close();
		} catch(Exception e) {
			System.out.println("failed to open " + args[2] );
			e.printStackTrace();
			exit_function(0);
		}
		// end reading the statement file
		// check for a valid statement
		if( !valid_expression( statement1 ) ) {
			System.out.println("invalid statement");
			exit_function(0);
		}
		
		boolean output1 = ttEntails.ttEntails(knowledge_base, statement1, model);
		boolean output2 = ttEntails.ttEntails(knowledge_base, statement2, model);

		try {
			outputStream = new BufferedWriter(new FileWriter(new File("result.txt")));
			if (output1 != output2) {
				System.out.println("definitely " + output1);
				outputStream.write("definitely " + output1);
			} else if (output1 == output2 && output1 == false) {
				System.out.println("possibly true, possibly false");
				outputStream.write("possibly true, possibly false");
			} else if (output1 == output2 && output1 == true) {
				System.out.println("both true and false");
				outputStream.write("both true and false");
			}
			outputStream.close();
		} catch (IOException e) {
			System.out.println("Error message : " + e.getMessage());
			e.printStackTrace();
		}
	} //end of main

	private static boolean isValidInput(String alpha, Set<String> set) {
		// TODO Auto-generated method stub
		Iterator<String> i = set.iterator();
		boolean bool = false;
		while(i.hasNext()) {
			if(i.next().equals(alpha))
				bool = true;
		}
		if(alpha.contains("(or") || alpha.contains("(and") || alpha.contains("(xor") || alpha.contains("(not") || alpha.contains("(if")	|| alpha.contains("(iff"))
			bool = true;
		return bool;
	}

	private static void getSymbols(LogicalExpression logEx) {
		// TODO Auto-generated method stub
		if(!(logEx.getUniqueSymbol() == null))
			listOfSymbols.add(logEx.getUniqueSymbol());
		else {
			for(int i = 0; i < logEx.getSubexpressions().size(); i++) {
				LogicalExpression logEx1 = logEx.getSubexpressions().get(i);
				getSymbols(logEx1);
				if(!(logEx1.getUniqueSymbol() == null))
					listOfSymbols.add(logEx1.getUniqueSymbol());
			}
		}
	}

	/* this method reads logical expressions
	 * if the next string is a:
	 * - '(' => then the next 'symbol' is a subexpression
	 * - else => it must be a unique_symbol
	 * 
	 * it returns a logical expression
	 * 
	 * notes: i'm not sure that I need the counter
	 * 
	 */
	public static LogicalExpression readExpression( String input_string ) 
	{
		LogicalExpression result = new LogicalExpression();
		//trim the whitespace off
		input_string = input_string.trim();
		if( input_string.startsWith("(") ) 
		{
			//its a subexpression
			String symbolString = "";
			// remove the '(' from the input string
			symbolString = input_string.substring( 1 );
			if( !symbolString.endsWith(")" ) ) 
			{
				// missing the closing paren - invalid expression
				System.out.println("missing ')' !!! - invalid expression! - readExpression():-" + symbolString );
				exit_function(0);
			}
			else 
			{
				//remove the last ')'
				//it should be at the end
				symbolString = symbolString.substring( 0 , ( symbolString.length() - 1 ) );
				symbolString.trim();
				// read the connective into the result LogicalExpression object					  
				symbolString = result.setConnective( symbolString );
			}
			//read the subexpressions into a vector and call setSubExpressions( Vector );
			result.setSubexpressions( read_subexpressions( symbolString ) );
		} 
		else 
		{   	
			// the next symbol must be a unique symbol
			// if the unique symbol is not valid, the setUniqueSymbol will tell us.
			result.setUniqueSymbol( input_string );
		}
		return result;
	}

	/* this method reads in all of the unique symbols of a subexpression
	 * the only place it is called is by read_expression(String, long)(( the only read_expression that actually does something ));
	 * 
	 * each string is EITHER:
	 * - a unique Symbol
	 * - a subexpression
	 * - Delineated by spaces, and paren pairs
	 * 
	 * it returns a vector of logicalExpressions
	 * 
	 * 
	 */

	public static Vector<LogicalExpression> read_subexpressions( String input_string ) {

		Vector<LogicalExpression> symbolList = new Vector<LogicalExpression>();
		LogicalExpression newExpression;// = new LogicalExpression();
		String newSymbol = new String();
		input_string.trim();

		while( input_string.length() > 0 ) {
			newExpression = new LogicalExpression();
			if( input_string.startsWith( "(" ) ) {
				//its a subexpression.
				// have readExpression parse it into a LogicalExpression object
				// find the matching ')'
				int parenCounter = 1;
				int matchingIndex = 1;
				while( ( parenCounter > 0 ) && ( matchingIndex < input_string.length() ) ) {
					if( input_string.charAt( matchingIndex ) == '(') {
						parenCounter++;
					} else if( input_string.charAt( matchingIndex ) == ')') {
						parenCounter--;
					}
					matchingIndex++;
				}
				// read untill the matching ')' into a new string
				newSymbol = input_string.substring( 0, matchingIndex );
				// pass that string to readExpression,
				newExpression = readExpression( newSymbol );
				// add the LogicalExpression that it returns to the vector symbolList
				symbolList.add( newExpression );
				// trim the logicalExpression from the input_string for further processing
				input_string = input_string.substring( newSymbol.length(), input_string.length() );
			} else {
				//its a unique symbol ( if its not, setUniqueSymbol() will tell us )
				// I only want the first symbol, so, create a LogicalExpression object and
				// add the object to the vector
				if( input_string.contains( " " ) ) {
					//remove the first string from the string
					newSymbol = input_string.substring( 0, input_string.indexOf( " " ) );
					input_string = input_string.substring( (newSymbol.length() + 1), input_string.length() );
				} else {
					newSymbol = input_string;
					input_string = "";
				}
				newExpression.setUniqueSymbol( newSymbol );
				symbolList.add( newExpression );
			}
			input_string.trim();
			if( input_string.startsWith( " " )) {
				//remove the leading whitespace
				input_string = input_string.substring(1);
			}
		}
		return symbolList;
	}

	/* this method checks to see if a logical expression is valid or not 
	 * a valid expression either:
	 * ( this is an XOR )
	 * - is a unique_symbol
	 * - has:
	 *  -- a connective
	 *  -- a vector of logical expressions
	 *  
	 * */
	public static boolean valid_expression(LogicalExpression expression)
	{
		// checks for an empty symbol
		// if symbol is not empty, check the symbol and
		// return the truthiness of the validity of that symbol
		if ( !(expression.getUniqueSymbol() == null) && ( expression.getConnective() == null ) ) {
			// we have a unique symbol, check to see if its valid
			return valid_symbol( expression.getUniqueSymbol() );
		}
		// symbol is empty, so
		// check to make sure the connective is valid
		// check for 'if / iff'
		if ( ( expression.getConnective().equalsIgnoreCase("if") )  ||
				( expression.getConnective().equalsIgnoreCase("iff") ) ) {
			// the connective is either 'if' or 'iff' - so check the number of connectives
			if (expression.getSubexpressions().size() != 2) {
				System.out.println("error: connective \"" + expression.getConnective() +
						"\" with " + expression.getSubexpressions().size() + " arguments\n" );
				return false;
			}
		}
		// end 'if / iff' check
		// check for 'not'
		else   if ( expression.getConnective().equalsIgnoreCase("not") ) {
			// the connective is NOT - there can be only one symbol / subexpression
			if ( expression.getSubexpressions().size() != 1)
			{
				System.out.println("error: connective \""+ expression.getConnective() + "\" with "+ expression.getSubexpressions().size() +" arguments\n" ); 
				return false;
			}
		}
		// end check for 'not'
		// check for 'and / or / xor'
		else if ( ( !expression.getConnective().equalsIgnoreCase("and") )  &&
				( !expression.getConnective().equalsIgnoreCase( "or" ) )  &&
				( !expression.getConnective().equalsIgnoreCase("xor" ) ) ) {
			System.out.println("error: unknown connective " + expression.getConnective() + "\n" );
			return false;
		}
		// end check for 'and / or / not'
		// end connective check
		// checks for validity of the logical_expression 'symbols' that go with the connective
		for( Enumeration<LogicalExpression> e = expression.getSubexpressions().elements(); e.hasMoreElements(); ) {
			LogicalExpression testExpression = (LogicalExpression)e.nextElement();
			// for each subExpression in expression,
			//check to see if the subexpression is valid
			if( !valid_expression( testExpression ) ) {
				return false;
			}
		}
		// if the method made it here, the expression must be valid
		return true;
	}

	/** this function checks to see if a unique symbol is valid */
	//////////////////// this function should be done and complete
	// originally returned a data type of long.
	// I think this needs to return true /false
	//public long valid_symbol( String symbol ) {
	public static boolean valid_symbol( String symbol ) {
		if (  symbol == null || ( symbol.length() == 0 )) {
			return false;
		}

		for ( int counter = 0; counter < symbol.length(); counter++ ) {
			if ( (symbol.charAt( counter ) != '_') &&
					( !Character.isLetterOrDigit( symbol.charAt( counter ) ) ) ) {
				System.out.println("String: " + symbol + " is invalid! Offending character:---" + symbol.charAt( counter ) + "---\n");
				return false;
			}
		}
		// the characters of the symbol string are either a letter or a digit or an underscore,
		//return true
		return true;
	}

	private static void exit_function(int value) {
		System.out.println("exiting from checkTrueFalse");
		System.exit(value);
	}	
}

class TTEntails {
	Set<String> symbolList = new HashSet<String>();	
	int counter = 0;

	public boolean ttEntails(LogicalExpression knowledge_base, LogicalExpression statement, Model model) {
		List<String> symbolList = getSymbols(knowledge_base, statement);
		symbolList = removeSymbols(model,symbolList);
		return ttCheckAll(knowledge_base, statement, symbolList, model);
	}

	private List<String> removeSymbols(Model model, List<String> symbolList2) {
		Iterator<Entry<String,Boolean>> i = model.hashMap.entrySet().iterator();
		while (i.hasNext()) {	    	
			Entry<String,Boolean> pair = (Entry<String,Boolean>)i.next();
			symbolList2.remove(pair.getKey());	       
		}
		return symbolList2;
	}

	boolean pl_True(LogicalExpression kb, Model model){
		Vector<LogicalExpression> vector = kb.getSubexpressions();
		Boolean bool = false;

		if( kb.getConnective() == null ) {						
			return model.hashMap.get(kb.getUniqueSymbol());			
		}
		else if(kb.getConnective()!=null && kb.getConnective().equalsIgnoreCase("not")){			
			return !(pl_True(kb.getNextSubexpression(),model));
		}
		else if(kb.getConnective()!=null && kb.getConnective().equalsIgnoreCase("or")){			
			for(int i=0;i<vector.size();i++){
				bool = bool || pl_True(vector.get(i),model);
			}
			return bool;		
		}
		else if(kb.getConnective()!=null && kb.getConnective().equalsIgnoreCase("if")){		
			bool = !(bool && !(pl_True(vector.get(1),model)));
			return bool;			
		}
		else if(kb.getConnective()!=null && kb.getConnective().equalsIgnoreCase("iff")){			
			return bool == pl_True(vector.get(1),model);
		}
		else if(kb.getConnective()!=null && kb.getConnective().equalsIgnoreCase("and")){			
			bool = true;
			for(int i = 0; i < vector.size(); i++){				
				bool = bool && pl_True(vector.get(i),model);
				if(bool==false){	
					return bool;
				}
			}
			return bool;
		}
		else if(kb.getConnective()!=null && kb.getConnective().equalsIgnoreCase("xor")){			
			int truthCounter=0;
			for(int i = 0; i < vector.size(); i++){
				boolean retrieved = pl_True(vector.get(i),model);
				if(retrieved==true)
					truthCounter++;
				if(truthCounter>1)
					return false;
				bool = ((bool||retrieved) && !(bool && retrieved));
			}
			return bool;
		}
		return true;
	}

	public boolean ttCheckAll(LogicalExpression kb, LogicalExpression alpha,	List<String> symbols, Model model) {		
		if (symbols.isEmpty()) {			
			boolean pl_true = pl_True(kb, model);			
			if(pl_true)
				return pl_True(alpha, model);				
			else
				return true;		
		} else {
			String P = (String)symbols.get(0);			
			List<String> rest = symbols.subList(1, symbols.size());			
			Model trueModel = model.extend(P, true);
			Model falseModel = model.extend(P, false);
			return (ttCheckAll(kb, alpha, rest, trueModel) && (ttCheckAll(kb, alpha, rest, falseModel)));
		}		
	}

	List<String> getSymbols(LogicalExpression kb, LogicalExpression alpha){		
		getSymbols(kb);
		getSymbols(alpha);		
		List<String> list = new ArrayList<String>(symbolList);
		return list;
	}

	void getSymbols(LogicalExpression logEx){
		if(!(logEx.getUniqueSymbol() == null))
			symbolList.add(logEx.getUniqueSymbol());
		else {
			for(int i = 0 ; i < logEx.getSubexpressions().size(); i++ ){
				LogicalExpression logEx1 = logEx.getSubexpressions().get(i);
				getSymbols(logEx1);
				if(!(logEx1.getUniqueSymbol() == null))
					symbolList.add(logEx1.getUniqueSymbol());			
			}
		}
	}		

	class Model{
		public HashMap<String,Boolean> hashMap = new HashMap<String,Boolean>();
		public Model extend(String symbol, boolean b) {
			Model model = new Model();
			model.hashMap.putAll(this.hashMap);
			model.hashMap.put(symbol, b);
			return model;
		}
	}
}