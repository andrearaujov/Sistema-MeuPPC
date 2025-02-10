import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import './Dashboard.css';
import { FaUserCircle, FaPlusCircle, FaPencilAlt, FaFileAlt } from 'react-icons/fa';
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
        } else if (decodedToken.papel === 'Avaliador') {
          url = '/api/avaliadores/ppcs';
        }

        const response = await axios.get(url, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        const ppcsEmCriacao = response.data.filter(ppc => ppc.status === 'Em Criacao');
        setPPCs(ppcsEmCriacao);
      } catch (error) {
        setError('Erro ao carregar PPCs');
      }
    };

    fetchPPCs();
  }, []);

  return (
    <div className="dashboard-container">
      <nav className="dashboard-navbar">
        <h1>PPC CRUD</h1>
        <ul className="dashboard-nav-links">
          <li><Link to="/dashboard">Home</Link></li>
          {(role === 'Coordenador' || role === 'Colaborador') && (
            <>
              <li><Link to="/ppcs">Gerenciar PPCs</Link></li>
              <li><Link to="/ppcs_ja_avaliados">PPCs Avaliados</Link></li>
              <li><Link to="/selecionar_ppc">Relatórios</Link></li>
              <li><Link to="/ppcs_avaliados">PPCs Avaliados Relatórios</Link></li>
            </>
          )}
          {role === 'Avaliador' && (
            <>
              <li><Link to="/ppcs/nao_avaliados">PPCs Não Avaliados</Link></li>
              <li><Link to="/ppcs/avaliados">PPCs Avaliados</Link></li>
            </>
          )}
          <li><Link to="/profile">Perfil</Link></li>
        </ul>
      </nav>
      <main>
        <header className="dashboard-header">
          <h2>PPCs Recentes</h2>
          {role === 'Coordenador' && (
            <Link to="/ppcs/create" className="dashboard-create-link">
              <FaPlusCircle /> Criar PPC
            </Link>
          )}
        </header>
        {error && <p className="dashboard-error">{error}</p>}
        <div className="dashboard-ppc-list">
          {ppcs.map((ppc) => (
            <div key={ppc.id} className="dashboard-ppc-item">
              <h3>{ppc.titulo}</h3>
              <p>{ppc.descricao}</p>
              {(role === 'Coordenador' || (role === 'Colaborador' && ppc.colaboradores.includes(String(userId)))) && (
                <Link to={`/ppcs/${ppc.id}`} className="dashboard-edit-link">
                  <FaPencilAlt /> Editar
                </Link>
              )}
              <Link to={`/ppcs/${ppc.id}/relatorio_colaboradores`} className="dashboard-report-link">
                <FaFileAlt /> Relatório de Colaboradores
              </Link>
              <Link to={`/ppcs/${ppc.id}/relatorio_avaliadores`} className="dashboard-report-link">
                <FaFileAlt /> Relatório de Avaliadores
              </Link>
              <Link to={`/ppcs/${ppc.id}/relatorio_participantes`} className="dashboard-report-link">
                <FaFileAlt /> Relatório de Participantes
              </Link>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
