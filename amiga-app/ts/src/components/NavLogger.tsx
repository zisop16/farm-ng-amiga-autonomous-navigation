import { useState, useEffect } from "react";
import { JsonView, allExpanded, defaultStyles } from "react-json-view-lite";
import "react-json-view-lite/dist/index.css";

function NavLogger() {
  const [gpsData, setGpsData] = useState<any>(null);
  const [isLogging, setIsLogging] = useState<boolean>(false);
  const [status, setStatus] = useState<string>("stopped");

  const startLogger = async () => {
    try {
      const response = await fetch(
        `${window.location.protocol}//${window.location.hostname}:8042/start_nav_logger`,
        { method: "POST" }
      );
      const result = await response.json();
      console.log("Start Logger:", result);
      setIsLogging(true);
      fetchLoggerStatus();
    } catch (error) {
      console.error("Error starting logger:", error);
    }
  };

  const stopLogger = async () => {
    try {
      const response = await fetch(
        `${window.location.protocol}//${window.location.hostname}:8042/stop_nav_logger`,
        { method: "POST" }
      );
      const result = await response.json();
      console.log("Stop Logger:", result);
      setIsLogging(false);
      fetchLoggerStatus();
    } catch (error) {
      console.error("Error stopping logger:", error);
    }
  };

  const fetchLoggerStatus = async () => {
    try {
      const response = await fetch(
        `${window.location.protocol}//${window.location.hostname}:8042/logger_status`
      );
      const result = await response.json();
      setStatus(result.status);
      setIsLogging(result.status === "running");
    } catch (error) {
      console.error("Error fetching logger status:", error);
    }
  };

  const fetchGpsLog = async () => {
    try {
      const response = await fetch(
        `${window.location.protocol}//${window.location.hostname}:8042/get_gps_log`
      );
      const result = await response.json();
      if (result.gps_coordinates) {
        setGpsData(result.gps_coordinates);
      }
    } catch (error) {
      console.error("Error fetching GPS log:", error);
    }
  };

  useEffect(() => {
    fetchLoggerStatus();
    const interval = setInterval(fetchLoggerStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (isLogging) {
      const ws = new WebSocket(
        `ws://${window.location.hostname}:8042/subscribe/gps/pvt`
      );

      ws.onmessage = (event) => {
        try {
          const receivedData = JSON.parse(event.data);
          setGpsData(receivedData);
        } catch (error) {
          console.error("Error parsing WebSocket message:", error);
        }
      };

      ws.onclose = () => {
        console.log("WebSocket closed");
      };

      return () => ws.close();
    }
  }, [isLogging]);

  return (
    <div>
      <h2>NavLogger Status: {status}</h2>
      <button onClick={startLogger} disabled={isLogging}>
        Start Logging
      </button>
      <button onClick={stopLogger} disabled={!isLogging}>
        Stop Logging
      </button>
      <button onClick={fetchGpsLog}>Fetch GPS Log</button>

      <div>
        {gpsData ? (
          <JsonView data={gpsData} shouldExpandNode={allExpanded} style={defaultStyles} />
        ) : (
          <p>No GPS Data Available</p>
        )}
      </div>
    </div>
  );
}

export default NavLogger;
