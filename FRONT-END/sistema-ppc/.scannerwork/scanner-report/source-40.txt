// frontend/src/components/PPCsAvaliados.jsx

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import {jwtDecode} from 'jwt-decode'; // Correção na importação
import './PPCsAvaliados.css';

const PPCsAvaliados = () => {
  const [ppcs, setPPCs] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchPPCs = async () => {
      try {
        const token = localStorage.getItem('token');
        const decodedToken = jwtDecode(token);

        const response = await axios.get('/api/avaliadores/ppcs/avaliados', {
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
            <h3>{ppc.titulo}</h3>
            <p>{ppc.descricao}</p>
            <p>Status: {ppc.status}</p>
            {ppc.motivo_rejeicao && <p>Motivo de Rejeição: {ppc.motivo_rejeicao}</p>}
          </div>
        ))}
      </div>
    </div>
  );
};

export default PPCsAvaliados;
