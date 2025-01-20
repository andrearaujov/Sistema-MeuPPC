import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, Link } from 'react-router-dom';
import './Relatorio.css';

const RelatorioParticipantes = () => {
  const { ppc_id } = useParams();
  const [participantes, setParticipantes] = useState({ colaboradores: [], avaliadores: [] });
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchParticipantes = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(`/api/ppcs/${ppc_id}/relatorio_participantes`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        setParticipantes(response.data);
      } catch (error) {
        setError('Erro ao carregar relatório de participantes');
      }
    };

    fetchParticipantes();
  }, [ppc_id]);

  return (
    <div className="relatorio-container">
      <h1>Relatório de Participantes</h1>
      <nav>
        <Link to="/dashboard" className="relatorio-back-link">Voltar</Link>
      </nav>
      {error && <p className="relatorio-error">{error}</p>}
      <h2>Colaboradores</h2>
      <ul>
        {participantes.colaboradores.map((colaborador) => (
          <li key={colaborador.id}>
            {colaborador.nome} - {colaborador.email}
          </li>
        ))}
      </ul>
      <h2>Avaliadores</h2>
      <ul>
        {participantes.avaliadores.map((avaliador) => (
          <li key={avaliador.id}>
            {avaliador.nome} - {avaliador.email}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default RelatorioParticipantes;
