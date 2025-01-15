import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './pages/Login/Login';
import Register from './pages/Register/Register';
import Dashboard from './pages/Dashboard/Dashboard';
import PPCs from './pages/PPC/PPCs';
import CreatePPC from './pages/PPC/CreatePPC';
import EditPPC from './pages/PPC/EditPPC';

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
        {/* Outras rotas */}
      </Routes>
    </Router>
  );
}

export default App;
