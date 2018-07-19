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

import org.apache.felix.scr.annotations.*;
import org.onosproject.net.Device;
import org.onosproject.net.device.DeviceService;
import org.onosproject.net.device.PortStatistics;
import org.rosuda.REngine.REXP;
import org.rosuda.REngine.Rserve.RConnection;

import java.util.List;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

/**
 * Skeletal ONOS application component.
 */
@Component(immediate = true)
public class AppComponent {

    //private final Logger log = LoggerFactory.getLogger(getClass());

    @Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
    protected DeviceService deviceService;

    private final int UNIT_K = 1024;
    private final int UNIT_B = 8;
    private final int UNIT_T = 5;

    @Activate
    protected void activate() {

        RConnection c = null;
        try {
            c = new RConnection();
            REXP x = c.eval("R.version.string");
            System.out.println("R version : " + x.asString());
            c.close();
        }catch(Exception e){
            e.printStackTrace();
        }
        ScheduledExecutorService executor = Executors.newSingleThreadScheduledExecutor();
        executor.scheduleAtFixedRate(this::monitorTraffic, 1, UNIT_T, TimeUnit.SECONDS);
    }

    @Deactivate
    protected void deactivate() {
    }

    private void monitorTraffic(){
        Iterable<Device> devices = deviceService.getDevices();
        for (Device device : devices) {
            List<PortStatistics> ports = deviceService.getPortDeltaStatistics(device.id());
            for (PortStatistics port : ports)
                System.out.println(device.id() + "\'s data: " + (double)port.bytesReceived() * UNIT_B / (UNIT_T * UNIT_K) + "Kbps");
        }
    }
}
