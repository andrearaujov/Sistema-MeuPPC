import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './pages/Login/Login';
import Register from './pages/Register/Register';
import Dashboard from './pages/Dashboard/Dashboard';
import PPCs from './pages/PPC/PPCs';
import CreatePPC from './pages/PPC/CreatePPC';
import EditPPC from './pages/PPC/EditPPC';
import AvaliarPPC from './pages/PPC/AvaliarPPC';
import PPCsNaoAvaliados from './pages/PPC/PPCsNaoAvaliados';
import PPCsAvaliados from './pages/PPC/PPCsAvaliados';
import PPCsJaAvaliados from './pages/PPC/PPCsJaAvaliados';
import Profile from './pages/Profile/Profile'; // Importando o componente de perfil

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/ppcs" element={<PPCs />} />
        <Route path="/ppcs/create" element={<CreatePPC />} />
        <Route path="/ppcs/:id" element={<EditPPC />} />
        <Route path="/avaliar/:id" element={<AvaliarPPC />} />
        <Route path="/ppcs/nao_avaliados" element={<PPCsNaoAvaliados />} />
        <Route path="/ppcs/avaliados" element={<PPCsAvaliados />} />
        <Route path="/ppcs_ja_avaliados" element={<PPCsJaAvaliados />} />
        <Route path="/profile" element={<Profile />} /> {/* Adicionando a rota de perfil */}
      </Routes>
    </Router>
  );
}

export default App;
