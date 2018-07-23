package start;

import mdp.MDP;

public class Start {
	final static int NUM_UES = 3;
	final static double FIG_DISCOUNT = 0.9;
	public static void main(String args[]) {
		new MDP(NUM_UES, FIG_DISCOUNT);
	}
}
