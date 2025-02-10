import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import './PPCsAvaliados.css';

const PPCsAvaliados = () => {
  const [ppcs, setPPCs] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchPPCs = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('/api/ppcs_avaliados', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        setPPCs(response.data);
      } catch (error) {
        setError('Erro ao carregar PPCs avaliados');
      }
    };

    fetchPPCs();
  }, []);

  return (
    <div className="ppcs-avaliados-container">
      <h1>PPCs Avaliados</h1>
      <nav>
        <Link to="/dashboard" className="ppcs-avaliados-back-link">Voltar</Link>
      </nav>
      {error && <p className="ppcs-avaliados-error">{error}</p>}
      <div className="ppcs-avaliados-list">
        {ppcs.map((ppc) => (
          <div key={ppc.id} className="ppcs-avaliados-item">
            <h2>{ppc.titulo}</h2>
            <p>{ppc.descricao}</p>
            <Link to={`/ppcs/${ppc.id}/relatorio_colaboradores`} className="ppcs-avaliados-report-link">
              Relatório de Colaboradores
            </Link>
            <Link to={`/ppcs/${ppc.id}/relatorio_avaliadores`} className="ppcs-avaliados-report-link">
              Relatório de Avaliadores
            </Link>
            <Link to={`/ppcs/${ppc.id}/relatorio_participantes`} className="ppcs-avaliados-report-link">
              Relatório de Participantes
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PPCsAvaliados;
