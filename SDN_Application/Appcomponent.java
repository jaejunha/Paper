package kr.ac.postech.app;

@Activate
protected void activate() {
	appId = coreService.registerApplication("org.iris4sdn.mesh");
        hostService.addListener(hostListener);
        log.info("Started");

        ScheduledExecutorService executor = Executors.newSingleThreadScheduledExecutor();
        executor.scheduleAtFixedRate(this::monitorTraffic, 1, 5, TimeUnit.SECONDS);
}

private void monitorTraffic(){
        Iterable<Device> devices = deviceService.getDevices();
        for (Device device : devices) {
            log.info("device: "+device.id());
            List<PortStatistics> ports = deviceService.getPortDeltaStatistics(device.id());
            for (PortStatistics port : ports)
                log.info("data: "+port.bytesReceived());
        }
}