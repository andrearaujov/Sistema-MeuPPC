import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import './Dashboard.css';
import { FaUserCircle, FaPlusCircle, FaPencilAlt } from 'react-icons/fa';

const Dashboard = () => {
  const [ppcs, setPPCs] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchPPCs = async () => {
      try {
        const token = localStorage.getItem('token');  // Supondo que o token JWT esteja armazenado no localStorage
        const response = await axios.get('/api/ppcs', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        setPPCs(response.data);
      } catch (error) {
        setError('Erro ao carregar PPCs');
      }
    };
  
    fetchPPCs();
  }, []);
  

  return (
    <div className="dashboard-container">
      <nav className="navbar">
        <h1>Dashboard</h1>
        <ul className="nav-links">
          <li><Link to="/dashboard">Home</Link></li>
          <li><Link to="/ppcs">Gerenciar PPCs</Link></li>
          <li><Link to="/profile">Perfil</Link></li>
        </ul>
      </nav>
      <main>
        <header>
          <h2>PPCs Recentes</h2>
          <Link to="/ppcs/create" className="create-link">
            <FaPlusCircle /> Criar PPC
          </Link>
        </header>
        {error && <p className="error">{error}</p>}
        <div className="ppc-list">
          {ppcs.map((ppc) => (
            <div key={ppc.id} className="ppc-item">
              <h3>{ppc.titulo}</h3>
              <p>{ppc.descricao}</p>
              <Link to={`/ppcs/${ppc.id}`} className="edit-link">
                <FaPencilAlt /> Editar
              </Link>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
