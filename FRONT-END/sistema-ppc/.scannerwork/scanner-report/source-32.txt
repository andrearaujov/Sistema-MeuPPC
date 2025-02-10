import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, Link } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';
import './AvaliarPPC.css';

const AvaliarPPC = () => {
  const { id } = useParams();
  const [ppc, setPPC] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchPPC = async () => {
      try {
        const token = localStorage.getItem('token');
        const decodedToken = jwtDecode(token);
        if (decodedToken.papel !== 'Avaliador') {
          setError('Você não tem permissão para avaliar este PPC');
          return;
        }

        const response = await axios.get(`/api/ppcs/${id}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });

        setPPC(response.data);
      } catch (error) {
        setError('Erro ao carregar PPC');
      }
    };

    fetchPPC();
  }, [id]);

  return (
    <div className="avaliar-ppc-container">
      <h1>Avaliar PPC</h1>
      <nav>
        <Link to="/dashboard" className="avaliar-ppc-back-btn">Voltar</Link>
      </nav>
      {error && <p className="avaliar-ppc-error">{error}</p>}
      {ppc && (
        <div className="avaliar-ppc-details">
          <h2>{ppc.titulo}</h2>
          <p>{ppc.descricao}</p>
        </div>
      )}
    </div>
  );
};

export default AvaliarPPC;
