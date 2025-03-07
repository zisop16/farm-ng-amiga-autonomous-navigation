import NavLogger from "./NavLogger";
import ExitButton from "./ExitButton";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>NavLogger</h1>
        <NavLogger />
      </header>
      <ExitButton />
    </div>
  );
}

export default App;
