import { BrowserRouter, Route, Routes} from 'react-router-dom';
import MainView from './MainView.js';
import './App.css';

function App() {

  return (
    <div className="appContainer">
      <BrowserRouter>
        <Routes>
          <Route path='/' element={<MainView />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
