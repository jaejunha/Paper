package mdp;

import mdp.object.UserEntity;
import q_learning.Q_Learning;

public class MDP {
	private UserEntity list_ue[];
	private double double_discount;
	
	public MDP(int numberOfUEs, double discount){
		initValues(numberOfUEs,discount);
		new Q_Learning();
	}
	
	private void initValues(int numberOfUEs, double discount){
		for(int i=0;i<numberOfUEs;i++)
			list_ue[i] = new UserEntity();
		double_discount = discount;
	}
	
	public double getDiscount() {
		return double_discount;
	}
	
	public void setDiscount(double discount) {
		double_discount = discount;
	}
	
	public UserEntity getUE(int i) {
		return list_ue[i];
	}
	
	public void setUE(int i, int j, double bandwidth) {
		list_ue[i].setAPIndex(j);
		list_ue[i].setBandwidth(bandwidth);
	}
}
