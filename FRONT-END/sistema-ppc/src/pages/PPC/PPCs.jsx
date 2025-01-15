import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import './PPCs.css';

const PPCs = () => {
  const [ppcs, setPPCs] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchPPCs = async () => {
      try {
        const response = await axios.get('/api/ppcs');
        setPPCs(response.data);
      } catch (error) {
        setError('Erro ao carregar PPCs');
      }
    };

    fetchPPCs();
  }, []);

  return (
    <div>
      <h1>Gerenciamento de PPCs</h1>
      {error && <p className="error">{error}</p>}
      <div className="ppc-list">
        {ppcs.map((ppc) => (
          <div key={ppc.id} className="ppc-item">
            <h2>{ppc.titulo}</h2>
            <p>{ppc.descricao}</p>
            <Link to={`/ppcs/${ppc.id}`}>Editar</Link>
          </div>
        ))}
      </div>
      <Link to="/ppcs/create" className="create-link">Criar Novo PPC</Link>
    </div>
  );
};

export default PPCs;
