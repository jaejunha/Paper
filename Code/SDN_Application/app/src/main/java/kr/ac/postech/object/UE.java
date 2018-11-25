package kr.ac.postech.object;

import java.util.ArrayList;
import java.util.Random;

public class UE {
    private double reqBitrate;
    private double reqQuality;
    private double bitrate;
    private double quality;
    private int ap;
    private ArrayList<Integer> rssi;

    public UE(int m){
        Random random = new Random();
        reqBitrate = MPD.bitrates[random.nextInt(5)];
        calQuality();

        rssi = new ArrayList<Integer>();
        rssi.add(0);
        for(int i=0;i<m;i++)
            rssi.add(-(random.nextInt(70)+30));
    }

    public double getReqBitrate() {
        return reqBitrate;
    }

    public void setReqBitrate(double reqBitrate) {
        this.reqBitrate = reqBitrate;
    }

    public double getReqQuality() {
        return reqQuality;
    }

    public void setReqQuality(double reqQuality) {
        this.reqQuality = reqQuality;
    }

    public double getBitrate() {
        return bitrate;
    }

    public void setBitrate(double bitrate) {
        this.bitrate = bitrate;
    }

    public double getQuality() {
        return quality;
    }

    public void setQuality(double quality) {
        this.quality = quality;
    }

    public int getAp() {
        return ap;
    }

    public void setAp(int ap) {
        this.ap = ap;
    }

    public ArrayList<Integer> getRssi() {
        return rssi;
    }

    public void setRssi(ArrayList<Integer> rssi) {
        this.rssi = rssi;
    }

    public void calQuality() {
        int a = 1, b = 1;
        reqQuality = a * Math.log(1 + b * reqBitrate);
    }
}

