import TopicMonitor from "./TopicMonitor";
import ExitButton from "./ExitButton";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Farm-ng Monitor</h1>
        <TopicMonitor />
      </header>
      <ExitButton />
    </div>
  );
}

export default App;
