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
    <div>
      <h1>Avaliar PPC</h1>
      <nav>
        <Link to="/dashboard">Voltar</Link>
      </nav>
      {error && <p className="error">{error}</p>}
      {ppc && (
        <div className="ppc-details">
          <h2>{ppc.titulo}</h2>
          <p>{ppc.descricao}</p>
          {ppc.arquivo && (
            <div>
              <h3>Arquivo Anexado:</h3>
              <a href={`http://localhost:5000/download/${ppc.arquivo}`} target="_blank" rel="noopener noreferrer">
                Baixar Arquivo
              </a>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default AvaliarPPC;
