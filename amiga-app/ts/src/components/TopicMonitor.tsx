import { useState, useEffect } from 'react';
import { JsonView, allExpanded, defaultStyles } from 'react-json-view-lite';
import 'react-json-view-lite/dist/index.css';

function TopicMonitor() {
    const [uris, setUris] = useState<string[]>([]);
    const [selectedUri, setSelectedUri] = useState<string>('');
    const [details, setDetails] = useState<any>(null);
    const pollInterval = 2000; // Interval in milliseconds to poll for data

    const fetchData = async () => {
        try {
            // Replace with your backend URL
            const response = await fetch(
                `${window.location.protocol}//${window.location.hostname}:${window.location.port}/list_uris`
            );
            // Check if the request was successful
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            const rawData = await response.json();
            return Object.keys(rawData);
        } catch (error) {
            console.error('Error fetching data:', error);
            return [];
        }
    };

    useEffect(() => {
        const pollData = async () => {
            let urisList = await fetchData();
            while (urisList.length === 0) {
                await new Promise(resolve => setTimeout(resolve, pollInterval));
                urisList = await fetchData();
            }
            setUris(urisList);
            setSelectedUri(urisList[0]);
        };

        pollData();
    }, []);

    useEffect(() => {
        if (!selectedUri) return;

        const detailSocket = new WebSocket(
            `ws://${window.location.hostname}:8042/subscribe/${selectedUri}`
        );

        detailSocket.onopen = (event) => {
            console.log('Detail WebSocket connection opened:', event);
        };

        detailSocket.onmessage = (event) => {
            const receivedDetails = JSON.parse(event.data);
            setDetails(receivedDetails);
        }

        detailSocket.onclose = (event) => {
            console.log('Detail WebSocket connection closed:', event);
        };

        return () => {
            detailSocket.close();
        };
    }, [selectedUri]);

    return (
        <div>
            <select value={selectedUri} onChange={(e) => setSelectedUri(e.target.value)}>
                {uris.map((uri, index) =>
                    <option key={index} value={uri}>
                        {uri}
                    </option>
                )}
            </select>

            <div>
                {selectedUri && (
                    <JsonView data={details} shouldExpandNode={allExpanded} style={defaultStyles} />
                )}
            </div>
        </div>
    );
}

export default TopicMonitor;
