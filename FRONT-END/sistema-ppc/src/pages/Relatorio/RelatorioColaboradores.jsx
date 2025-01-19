// frontend/src/pages/Relatorio/RelatorioColaboradores.jsx

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, Link } from 'react-router-dom';
import './Relatorio.css';

const RelatorioColaboradores = () => {
  const { ppc_id } = useParams();
  const [colaboradores, setColaboradores] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchColaboradores = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(`/api/ppcs/${ppc_id}/relatorio_colaboradores`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        setColaboradores(response.data);
      } catch (error) {
        setError('Erro ao carregar relatório de colaboradores');
      }
    };

    fetchColaboradores();
  }, [ppc_id]);

  return (
    <div className="relatorio-container">
      <h1>Relatório de Colaboradores</h1>
      <nav>
        <Link to="/dashboard">Voltar</Link>
      </nav>
      {error && <p className="error">{error}</p>}
      <ul>
        {colaboradores.map((colaborador) => (
          <li key={colaborador.id}>
            {colaborador.nome} - {colaborador.email}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default RelatorioColaboradores;
