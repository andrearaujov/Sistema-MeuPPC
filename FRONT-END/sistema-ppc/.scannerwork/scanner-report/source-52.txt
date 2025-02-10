import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, Link } from 'react-router-dom';
import './Relatorio.css';

const RelatorioAvaliadores = () => {
  const { ppc_id } = useParams();
  const [avaliadores, setAvaliadores] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchAvaliadores = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(`/api/ppcs/${ppc_id}/relatorio_avaliadores`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        setAvaliadores(response.data);
      } catch (error) {
        setError('Erro ao carregar relatório de avaliadores');
      }
    };

    fetchAvaliadores();
  }, [ppc_id]);

  return (
    <div className="relatorio-container">
      <h1>Relatório de Avaliadores</h1>
      <nav>
        <Link to="/dashboard" className="relatorio-back-link">Voltar</Link>
      </nav>
      {error && <p className="relatorio-error">{error}</p>}
      <ul>
        {avaliadores.map((avaliador) => (
          <li key={avaliador.id}>
            {avaliador.nome} - {avaliador.email}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default RelatorioAvaliadores;
