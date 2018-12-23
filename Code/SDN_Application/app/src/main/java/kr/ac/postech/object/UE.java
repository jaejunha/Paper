package kr.ac.postech.object;

import kr.ac.postech.util.Util;

import java.util.ArrayList;
import java.util.Random;

public class UE implements Comparable<UE>{
    private int id;
    private int reqBitrate;
    private double reqQuality;
    private int bitrate;
    private double quality;
    private int ap;
    private ArrayList<Integer> rssi;

    public UE(){
        reqBitrate = 0;
    }

    public UE(int id, int m){
        this.id = id;
        Random random = new Random();
        reqBitrate = MPD.bitrates[random.nextInt(5)];
        reqQuality = Util.calQuality(reqBitrate);

        rssi = new ArrayList<Integer>();
        rssi.add(0);
        for(int i=0;i<m;i++)
            rssi.add(-(random.nextInt(70)+30));
    }

    public int getID(){ return id; }

    public void setID(int id) { this.id = id; }

    public int getReqBitrate() {
        return reqBitrate;
    }

    public void setReqBitrate(int reqBitrate) {
        this.reqBitrate = reqBitrate;
    }

    public double getReqQuality() {
        return reqQuality;
    }

    public void setReqQuality(double reqQuality) {
        this.reqQuality = reqQuality;
    }

    public int getBitrate() {
        return bitrate;
    }

    public void setBitrate(int bitrate) {
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

    @Override
    public int compareTo(UE ue) {
        // TODO Auto-generated method stub
        return this.reqBitrate - ue.reqBitrate;
    }
}

