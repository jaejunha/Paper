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

import kr.ac.postech.object.UE;
import org.apache.felix.scr.annotations.*;
import org.onosproject.net.Device;
import org.onosproject.net.Port;
import org.onosproject.net.device.DeviceService;
import org.onosproject.net.device.PortStatistics;
import org.rosuda.REngine.REXP;
import org.rosuda.REngine.Rserve.RConnection;

import java.util.HashMap;
import java.util.List;
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

/**
 * Skeletal ONOS application component.
 */
@Component(immediate = true)
public class AppComponent {

    //private final Logger log = LoggerFactory.getLogger(getClass());

    @Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
    protected DeviceService deviceService;

    private final int MAX_M = 100;
    private final int MAX_N = 100;
    private final int MAX_T = 500;

    private final int UNIT_K = 1024;
    private final int UNIT_B = 8;
    private final int UNIT_T = 5;

    private final int INT_NUM_CLIENT = 10;
    private final int INT_PORT = 7777;

    HashMap<String, String> hash_type;

    @Activate
    protected void activate() {

        new UE();

    //Initiation
        hash_type = new HashMap<String, String>();

	//To test R library
        RConnection c = null;
        try {
            c = new RConnection();
            REXP x = c.eval("R.version.string");
            System.out.println("R version : " + x.asString());
            c.close();
        }catch(Exception e){
            e.printStackTrace();
        }

	//To collect Bandwidth information
        ScheduledExecutorService executor_monitor = Executors.newSingleThreadScheduledExecutor();
        executor_monitor.scheduleAtFixedRate(this::monitorTraffic, 1, UNIT_T, TimeUnit.SECONDS);

	//To collect RSSI information
	try{
		ServerSocket socket_server = new ServerSocket(INT_PORT);
		ExecutorService executor_pool = Executors.newFixedThreadPool(INT_NUM_CLIENT);
		while(true)
			executor_pool.execute(new ServerThread(socket_server.accept()));	
	}catch(Exception e){
		e.printStackTrace();
	}
    }

    @Deactivate
    protected void deactivate() {
    }

    private void monitorTraffic(){
        Iterable<Device> devices = deviceService.getDevices();
        for (Device device : devices) {
            Port port = deviceService.getPorts(device.id()).get(1);
            String str_portName = port.annotations().value("portName");
            if(str_portName.equals("ap0"))
                hash_type.put(device.id().toString(), "AP");
            else
                hash_type.put(device.id().toString(),"UE");
            System.out.println(hash_type.get(device.id().toString()));
            for (PortStatistics statistics : deviceService.getPortDeltaStatistics(device.id()))
                System.out.println(device.id() + "\'s data: " + (double) statistics.bytesReceived() * UNIT_B / (UNIT_T * UNIT_K) + "Kbps");
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
			System.out.println("received: " + str_answer);

			PrintWriter writer = new PrintWriter(socket_client.getOutputStream(), true);
			writer.println("OK");
//			writer.println("nmcli dev wifi con SMALL_AP");
			socket_client.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
    }
}
