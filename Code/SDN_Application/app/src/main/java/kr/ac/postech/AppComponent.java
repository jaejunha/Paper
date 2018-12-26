/*
 * Copyright 2018-present Open Networking Foundation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package kr.ac.postech;

import kr.ac.postech.object.AP;
import kr.ac.postech.object.UE;
import kr.ac.postech.util.Util;
import org.apache.felix.scr.annotations.*;
import org.onosproject.net.Device;
import org.onosproject.net.Port;
import org.onosproject.net.device.DeviceService;
import org.onosproject.net.device.PortStatistics;
import org.rosuda.REngine.REXP;
import org.rosuda.REngine.Rserve.RConnection;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.concurrent.Executors;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Skeletal ONOS application component.
 */
@Component(immediate = true)
public class AppComponent {

    @Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
    protected DeviceService deviceService;

    private final int UNIT_K = 1024;
    private final int UNIT_B = 8;
    private final int UNIT_T = 5;

    private final int INT_PORT = 7777;

    private HashMap<String, String> hash_type;
    private static HashMap<String, HashMap<String, ArrayList<Integer>>> hash_rssi;
    private static HashMap<String, ArrayList<Double>> hash_bandwidth;
    private final static int SIZE_WINDOW = 5;

    private static Pattern p;
    private static Matcher m;

    /**************************************************************************
     MAX_M: the maximum # of AP
     MAX_N: the maximum # of UE
     MAX_T: the maximum # of time slot
     **************************************************************************/
    private final int MAX_M = 100;
    private final int MAX_N = 100;
    private final int MAX_T = 500;

    /**************************************************************************
     int_m: # of AP
     int_n: # of UE
     int_t: maximum time slot
     **************************************************************************/
    private int int_n;
    private int int_m;
    private int int_t;

    /**************************************************************************
     Information of UE and AP

     int_ueID: id of UE
     list_ue: list of UE information
     list_ap: list of AP information
     list_sortedUE: sorted list index of ue information in terms of required bitrate
     **************************************************************************/
    private int int_ueID = 1;
    private ArrayList<UE> list_ue;
    private ArrayList<AP> list_ap;
    private ArrayList<UE> list_sortedUE;

    /**************************************************************************
     Optimized value

     double_optimizedDifference:    optimized difference
     bool_optimizedP:			    optimized p
     list_optimizedBitrate:		    optimized bitrate
     **************************************************************************/
    private double double_optimizedDifference;
    private boolean bool_optimizedP[][];
    private ArrayList<Integer> list_optimizedBitrate;

    /**************************************************************************
     Relation between UE and AP

     bool_r: whether reachable or not
     bool_p: status of connection
     **************************************************************************/
    private boolean bool_r[][];
    private boolean bool_p[][];

    /**************************************************************************
     Success in finding appropriate handover
     **************************************************************************/
    boolean bool_end;

    @Activate
    protected void activate() {

        // To simulate, insert random values
        /*
        int_n = 4;
        int_m = 3;
        int_t = 20;

        list_ue = new ArrayList<>();
        list_ap = new ArrayList<>();

        list_ue.add(new UE());
        for (int i = 1; i <= int_n; i++)
            list_ue.add(new UE(int_ueID++, int_m));

        list_ap.add(new AP());
        for (int i = 1; i <= int_m; i++)
            list_ap.add(new AP());

        bool_r = new boolean[MAX_N + 1][MAX_M + 1];
        bool_p = new boolean[MAX_N + 1][MAX_M + 1];
        bool_optimizedP = new boolean[MAX_N + 1][MAX_M + 1];

        // UE 1 can be associated with AP 1
        bool_r[1][1] = true;
        // UE 2 can be associated with AP 1 and AP 3
        bool_r[2][1] = true;
        bool_r[2][3] = true;
        // UE 3 can be associated with AP 2 and AP 3
        bool_r[3][2] = true;
        bool_r[3][3] = true;
        // UE 4 can be associated with AP 3
        bool_r[4][3] = true;

        bool_end = false;

        // Initialize difference of bitrate and quality
        list_optimizedBitrate = new ArrayList<>();
        list_optimizedBitrate.add(new Integer(0));
        for(int i=1;i<=int_n;i++)
            list_optimizedBitrate.add(new Integer(0));
        double_optimizedDifference = Double.MAX_VALUE;

        printStatus();

        cloneListUE();

        dfs(1);

        printResult();

        */
/*

        //To test R library
        RConnection c = null;
        try {
            c = new RConnection();
            REXP x = c.eval("R.version.string");
            System.out.println("R version : " + x.asString());
            c.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
*/
        //To collect Bandwidth information
        hash_type = new HashMap<>();
        hash_bandwidth = new HashMap<>();

        ScheduledExecutorService executor_monitor = Executors.newSingleThreadScheduledExecutor();
        executor_monitor.scheduleAtFixedRate(this::monitorTraffic, 1, UNIT_T, TimeUnit.SECONDS);

        //To collect RSSI information

        hash_rssi = new HashMap<>();

/*
        try {
            ServerSocket socket_server = new ServerSocket(INT_PORT);
            ExecutorService executor_pool = Executors.newFixedThreadPool(MAX_N);
            while (true)
                executor_pool.execute(new ServerThread(socket_server.accept()));
        } catch (Exception e) {
            e.printStackTrace();
        }
        */
    }

    @Deactivate
    protected void deactivate() {
    }

    private void monitorTraffic() {
        Iterable<Device> devices = deviceService.getDevices();
        for (Device device : devices) {
            try {
                Port port = deviceService.getPorts(device.id()).get(1);
                String str_portName = port.annotations().value("portName");
                if (str_portName.equals("ap0"))
                    hash_type.put(device.id().toString(), "AP");
                else
                    hash_type.put(device.id().toString(), "UE");

                System.out.print(hash_type.get(device.id().toString()) + "(");
                double double_bandwidth, double_avg = 0;
                String str_mac;
                for (PortStatistics statistics : deviceService.getPortDeltaStatistics(device.id())) {
                    str_mac = device.id().toString();
                    double_bandwidth = (double) statistics.bytesReceived() * UNIT_B / (UNIT_T * UNIT_K);

                    if(hash_bandwidth.get(str_mac) == null) {
                        ArrayList<Double> list_bandwidth = new ArrayList<>();
                        list_bandwidth.add(double_bandwidth);
                        hash_bandwidth.put(str_mac, list_bandwidth);

                        double_avg = double_bandwidth;
                    }else{
                        if(hash_bandwidth.get(str_mac).size() < SIZE_WINDOW){
                            hash_bandwidth.get(str_mac).add(double_bandwidth);

                            double_avg = getBandwidthAVG(hash_bandwidth.get(str_mac));
                        }else{
                            hash_bandwidth.get(str_mac).remove(0);
                            hash_bandwidth.get(str_mac).add(double_bandwidth);

                            double_avg = getBandwidthAVG(hash_bandwidth.get(str_mac));
                        }
                    }
                    System.out.println(str_mac + "): " + double_avg + "Kbps");
                }
            }catch(java.lang.ArrayIndexOutOfBoundsException e){
                // ignore
            }
        }
    }

    static class ServerThread implements Runnable {
        private Socket socket_client = null;

        public ServerThread(Socket socket_client) {
            this.socket_client = socket_client;
        }

        @Override
        public void run() {
            // TODO Auto-generated method stub
            try {
                String str_answer = new BufferedReader(new InputStreamReader(socket_client.getInputStream())).readLine();
                
                if (str_answer != null) {
                    try {

                        String str_connectedAP = "";
                        String str_mac = "";
                        String str_rssis = "";
                        String str_bitrate_req = "";
                        String str_bitrate_sup = "";

                        p = Pattern.compile("\"REQ\": [0-9]+");
                        m = p.matcher(str_answer);
                        if(m.find())
                            str_bitrate_req = m.group().split(" ")[1];

                        p = Pattern.compile("\"SUP\": [0-9]+");
                        m = p.matcher(str_answer);
                        if(m.find())
                            str_bitrate_sup = m.group().split(" ")[1];

                        p = Pattern.compile("\"AP\": \"[^\"]*\"");
                        m = p.matcher(str_answer);
                        if(m.find())
                            str_connectedAP = m.group().split("\"")[3];

                        p = Pattern.compile("\"MAC\": \"[^\"]*\"");
                        m = p.matcher(str_answer);
                        if(m.find())
                            str_mac = m.group().split("\"")[3];

                        System.out.println("requested bitrate: " + str_bitrate_req);
                        System.out.println("supported bitrate: " + str_bitrate_sup);
                        System.out.println("Connected AP: " + str_connectedAP);
                        System.out.println("MAC address: " + str_mac);

                        if(hash_rssi.get(str_mac) == null)
                            hash_rssi.put(str_mac, new HashMap<>());

                        p = Pattern.compile("\"RSSI\": \\[.*\\]");
                        m = p.matcher(str_answer);
                        if(m.find())
                            str_rssis = m.group();
                        str_rssis = str_rssis.substring(str_rssis.indexOf("[") + 1, str_rssis.length() - 1).replace("\\]", "");
                        double double_avg = 0;
                        //double double_std = 0;

                        for(String str: str_rssis.split("\\[")) {
                            if(!str.equals("")) {
                                String str_ap = str.split("\"")[1];
                                Integer int_rssi = Integer.parseInt(str.split("\"")[3]);

                                if (hash_rssi.get(str_mac).get(str_ap) == null) {
                                    ArrayList<Integer> list_rssi = new ArrayList<>();
                                    list_rssi.add(int_rssi);
                                    hash_rssi.get(str_mac).put(str_ap, list_rssi);

                                    double_avg = int_rssi;
                                    //double_std = getSTD(hash_rssi.get(str_mac).get(str_ap), double_avg);
                                } else {
                                    if(hash_rssi.get(str_mac).get(str_ap).size() < SIZE_WINDOW) {
                                        hash_rssi.get(str_mac).get(str_ap).add(int_rssi);

                                        double_avg = getRSSIAVG(hash_rssi.get(str_mac).get(str_ap));
                                        //double_std = getSTD(hash_rssi.get(str_mac).get(str_ap), double_avg);
                                    }
                                    else {
                                        hash_rssi.get(str_mac).get(str_ap).remove(0);
                                        hash_rssi.get(str_mac).get(str_ap).add(int_rssi);

                                        double_avg = getRSSIAVG(hash_rssi.get(str_mac).get(str_ap));
                                        //double_std = getSTD(hash_rssi.get(str_mac).get(str_ap), double_avg);
                                    }
                                }
                                //System.out.println(double_avg+" "+double_std);
                                System.out.println(double_avg);
                            }
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                    /*
                    PrintWriter writer = new PrintWriter(socket_client.getOutputStream(), true);
                    writer.println("#2: LOAD_AP2");
                    */
                    socket_client.close();

                }
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }
    }

    public static double getBandwidthAVG(ArrayList<Double> list_bandwidth) {
        double double_sum = 0;
        for(Double bandwidth: list_bandwidth)
            double_sum+=bandwidth;

        return double_sum / list_bandwidth.size();
    }

    public static double getRSSIAVG(ArrayList<Integer> list_rssi) {
        double double_sum = 0;
        for(Integer rssi: list_rssi)
            double_sum+=rssi;
		
        return double_sum / list_rssi.size();
    }
	
    public static double getRSSISTD(ArrayList<Integer> list_rssi, double double_avg) {
        double double_sum = 0;
        for(Integer rssi: list_rssi)
            double_sum+=(rssi-double_avg)*(rssi-double_avg);
		
        return Math.sqrt(double_sum/list_rssi.size());
    }

    public void printStatus() {
        System.out.println("==========================================");
        for (int i = 1; i <= int_n; i++) {
            System.out.print("UE " + i + "(wants " + list_ue.get(i).getReqBitrate() + "bps) can be associated with");
            int int_count = 0;
            for (int j = 1; j <= int_m; j++) {
                if (bool_r[i][j]) {
                    if (int_count++ > 0)
                        System.out.print(",");
                    System.out.print(" AP " + j + "(" + list_ue.get(i).getRssi().get(j) + "dB)");
                }
            }
            System.out.println();
        }
        System.out.println("------------------------------------------");
    }

    public void cloneListUE() {
        if (list_sortedUE == null)
            list_sortedUE = new ArrayList<>();
        else
            list_sortedUE.clear();
        list_sortedUE.addAll(list_ue);
        Collections.sort(list_sortedUE);
    }

    public void dfs(int int_ue) {

        // End of DFS
        if (int_ue == int_n + 1) {
            // Calculate difference of quality
            double double_difference = 0;
            for (int i = 1; i <= int_n; i++)
                double_difference += Math.max(list_ue.get(i).getReqBitrate() - list_ue.get(i).getQuality(), (double)0);

            System.out.print("difference: " + String.format("%.6f",double_difference) + "\t");
            System.out.print("[");
            for (int i = 1; i <= int_n; i++) {
                System.out.print("(UE " + i + "-AP" + list_ue.get(i).getAp() + ", "+ list_ue.get(i).getBitrate() + "bps");
                if (i <= int_n - 1)
                    System.out.print(", ");
            }
            System.out.println(")]");

            // If optimized value is needed to changed
            if (double_difference < double_optimizedDifference) {
                double_optimizedDifference = double_difference;
                for (int i = 1; i <= int_n; i++) {
                    list_optimizedBitrate.set(i, list_ue.get(i).getBitrate());
                    for (int j = 1; j <= int_m; j++)
                        bool_optimizedP[i][j] = bool_p[i][j];
                }
            }

            if (double_optimizedDifference == 0)
                bool_end = true;

            return;
        }

        int int_sortedID = list_sortedUE.get(int_ue).getID();
        for (int i = 1; i <= int_m; i++) {

            // When cannot connect AP
            if (bool_r[int_sortedID][i] == false)
                continue;

            // When AP's time slot is full
            if (list_ap.get(i).getTimeSlot() == int_t)
                continue;

            bool_p[int_sortedID][i] = true;
            list_ue.get(int_sortedID).setAp(i);
            // Save values to restore later
            double double_apTimeSlot = list_ap.get(i).getTimeSlot();
            double double_ueTimeSlot = -(double)list_ue.get(int_sortedID).getReqBitrate() / list_ue.get(int_sortedID).getRssi().get(i);

            // AP has enough time slot
            if (double_ueTimeSlot + list_ap.get(i).getTimeSlot() <= int_t) {
                list_ue.get(int_sortedID).setBitrate(Util.findBitrate(list_ue.get(int_sortedID), double_ueTimeSlot, double_ueTimeSlot));
                list_ap.get(i).setTimeSlot(double_ueTimeSlot);
            }
            // AP has small time slot
            else {
                list_ue.get(int_sortedID).setBitrate(Util.findBitrate(list_ue.get(int_sortedID), int_t - list_ap.get(i).getTimeSlot(), double_ueTimeSlot));
                // If find bitrate in MPD
                if (list_ue.get(int_sortedID).getBitrate() > 0)
                    list_ap.get(i).setTimeSlot(int_t);
            }

            // Calculate quality
            list_ue.get(int_sortedID).setQuality(Util.calQuality(list_ue.get(int_sortedID).getBitrate()));

            // When Success, Check next UE
            if (list_ue.get(int_sortedID).getBitrate() > 0)
                dfs(int_ue + 1);

            // Success in finding appropriate handover
            if (bool_end)
                return;

            // Retore values
            list_ue.get(int_sortedID).setAp(0);
            bool_p[int_sortedID][i] = false;
            list_ap.get(i).setTimeSlot(double_apTimeSlot);
        }
    }

    public void printResult() {
        if (double_optimizedDifference == Double.MAX_VALUE)
            System.out.println("Fail to optimize");
        else {
            System.out.println("------------------------------------------");
            System.out.println("Optimized difference of total quality: " + double_optimizedDifference);
            System.out.println("Optimized connection ��");
            for (int i = 1; i <= int_n; i++) {
                System.out.print("UE " + i + "(" + list_optimizedBitrate.get(i) + "bps) is associated with AP ");
                for (int j = 1; j <= int_m; j++) {
                    if (bool_optimizedP[i][j]) {
                        System.out.println(j);
                        break;
                    }
                }
            }
        }
        System.out.println("==========================================");
        System.out.println();
    }
}
