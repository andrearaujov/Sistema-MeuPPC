import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';
import './PPCsNaoAvaliados.css';

const PPCsNaoAvaliados = () => {
  const [ppcs, setPPCs] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchPPCs = async () => {
      try {
        const token = localStorage.getItem('token');
        const decodedToken = jwtDecode(token);

        const response = await axios.get('/api/avaliadores/ppcs/nao_avaliados', {
          headers: { 'Authorization': `Bearer ${token}` }
        });

        setPPCs(response.data);
      } catch (error) {
        setError('Erro ao carregar PPCs não avaliados');
      }
    };

    fetchPPCs();
  }, []);

  return (
    <div>
      <h1>PPCs Não Avaliados</h1>
      <nav>
        <Link to="/dashboard">Voltar</Link>
      </nav>
      {error && <p className="error">{error}</p>}
      <div className="ppc-list">
        {ppcs.map((ppc) => (
          <div key={ppc.id} className="ppc-item">
            <h3>{ppc.titulo}</h3>
            <p>{ppc.descricao}</p>
            <Link to={`/avaliar/${ppc.id}`} className="edit-link">
              Avaliar
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PPCsNaoAvaliados;
