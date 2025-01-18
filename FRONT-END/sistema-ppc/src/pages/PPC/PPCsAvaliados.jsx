import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';
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
    <div>
      <h1>PPCs Avaliados</h1>
      <nav>
        <Link to="/dashboard">Voltar</Link>
      </nav>
      {error && <p className="error">{error}</p>}
      <div className="ppc-list">
        {ppcs.map((ppc) => (
          <div key={ppc.id} className="ppc-item">
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
