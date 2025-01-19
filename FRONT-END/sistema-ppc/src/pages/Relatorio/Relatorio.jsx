// frontend/src/pages/Relatorio/Relatorios.jsx

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import './Relatorio.css';

const Relatorios = () => {
  const [ppcs, setPPCs] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchPPCs = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('/api/ppcs_ja_avaliados', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        setPPCs(response.data);
      } catch (error) {
        setError('Erro ao carregar relatórios');
      }
    };

    fetchPPCs();
  }, []);

  return (
    <div className="relatorios-container">
      <h1>Relatórios de PPCs Avaliados</h1>
      {error && <p className="error">{error}</p>}
      <div className="relatorios-list">
        {ppcs.map((ppc) => (
          <div key={ppc.id} className="relatorio-item">
            <h2>{ppc.titulo}</h2>
            <p>{ppc.descricao}</p>
            <Link to={`/relatorio/${ppc.id}`} className="view-link">Ver Relatório</Link>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Relatorios;
