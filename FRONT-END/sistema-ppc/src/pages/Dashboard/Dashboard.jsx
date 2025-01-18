import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import './Dashboard.css';
import { FaUserCircle, FaPlusCircle, FaPencilAlt } from 'react-icons/fa';
import { jwtDecode } from 'jwt-decode';

const Dashboard = () => {
  const [ppcs, setPPCs] = useState([]);
  const [error, setError] = useState('');
  const [role, setRole] = useState('');
  const [userId, setUserId] = useState('');

  useEffect(() => {
    const fetchPPCs = async () => {
      try {
        const token = localStorage.getItem('token');
        const decodedToken = jwtDecode(token);
        setRole(decodedToken.papel);
        setUserId(decodedToken.id);

        let url = '/api/ppcs';
        if (decodedToken.papel === 'Colaborador') {
          url = '/api/colaboradores/ppcs';
        }

        const response = await axios.get(url, {
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
          {role === 'Coordenador' && (
            <Link to="/ppcs/create" className="create-link">
              <FaPlusCircle /> Criar PPC
            </Link>
          )}
        </header>
        {error && <p className="error">{error}</p>}
        <div className="ppc-list">
          {ppcs.map((ppc) => (
            <div key={ppc.id} className="ppc-item">
              <h3>{ppc.titulo}</h3>
              <p>{ppc.descricao}</p>
              {role === 'Coordenador' || (role === 'Colaborador' && ppc.colaboradores.includes(String(userId))) ? (
                <Link to={`/ppcs/${ppc.id}`} className="edit-link">
                  <FaPencilAlt /> Editar
                </Link>
              ) : (
                role === 'Avaliador' && ppc.status === 'Em Avaliacao' && (
                  <Link to={`/ppcs/${ppc.id}`} className="edit-link">
                    <FaPencilAlt /> Avaliar
                  </Link>
                )
              )}
            </div>
          ))}
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
