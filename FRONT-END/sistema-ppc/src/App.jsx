import "./App.css";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from "./pages/Login/Login";
import Register from "./pages/Register/Register"; // Importando o componente Register

function App() {
  return (
    <Router> {/* Envolva o app com o Router */}
      <div className="App">
        <Routes> {/* Defina as rotas aqui */}
          <Route path="/" element={<Login />} /> {/* Rota para Login */}
          <Route path="/register" element={<Register />} /> {/* Rota para Register */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
