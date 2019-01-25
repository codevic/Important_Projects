import java.io.BufferedWriter;
import java.io.FileWriter;
import java.text.DecimalFormat;
import java.io.IOException;

public class compute_a_posteriori{
	public static void main(String[] args)throws IOException{
		FileWriter f = new FileWriter("result.txt");
		BufferedWriter bw = new BufferedWriter(f);
		String seq = args[0];
		DecimalFormat format = new DecimalFormat("#.#####");
		int C = 0, L = 0;
		//the probability of picking up the cherry candy from the respective bag
		double[] pC = {1,0.75,0.5,0.25,0};
		double[] pHyp= {0.1,0.2,0.4,0.2,0.1};
		double[] pHyp_CL = new double[5];
		double sum = 0;
		for(int i = 0; i < seq.length() ; i++){
			if(seq.charAt(i) == 'C')	C+=1;
			else	L+=1;
		}		
		for(int i = 0; i < 5 ; i++)
		{
			pHyp_CL[i] = Math.pow(pC[i], C) * Math.pow((1-pC[i]), L) * (pHyp[i]);
			sum += pHyp_CL[i];
		}
		bw.write("Observation Sequence Q: "+seq);
		bw.newLine();
		bw.write("Length Q: "+seq.length());
		bw.newLine();
		for(int i = 0; i < 5 ; i++)
		{
			pHyp_CL[i] = pHyp_CL[i] * (1/sum);
			bw.write("P(h"+(i+1)+" |Q) = "+format.format(pHyp_CL[i]));
			bw.newLine();
		}
		sum = 0;
		for(int i=0;i<5;i++){
			sum = sum + (pC[i] * pHyp_CL[i]);
		}
		bw.newLine();
		bw.write("Probability that the next candy we pick will be C, given Q: "+format.format(sum));
		bw.newLine();
		bw.write("Probability that the next candy we pick will be L, given Q: "+format.format(1-sum));
		bw.newLine();
		bw.close();
		f.close();
	}
}