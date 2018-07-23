package mdp.object;

public class UserEntity {
	private double double_bandwidth;
	private int int_ap;
	
	public int getAPIndex() {
		return int_ap;
	}
	
	public void setAPIndex(int ap) {
		int_ap = ap;
	}
	
	public double getBandwidth() {
		return double_bandwidth;
	}
	
	public void setBandwidth(double bandwidth) {
		double_bandwidth = bandwidth;
	}
}
