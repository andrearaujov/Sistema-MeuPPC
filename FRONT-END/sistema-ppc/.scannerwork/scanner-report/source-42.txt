import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';
import './PPCsJaAvaliados.css';

const PPCsJaAvaliados = () => {
  const [ppcs, setPPCs] = useState([]);
  const [error, setError] = useState('');
  const [role, setRole] = useState('');

  useEffect(() => {
    const fetchPPCs = async () => {
      try {
        const token = localStorage.getItem('token');
        const decodedToken = jwtDecode(token);
        setRole(decodedToken.papel);

        let url = '/api/colaboradores/ppcs_avaliados';
        if (decodedToken.papel === 'Coordenador') {
          url = '/api/coordenadores/ppcs_avaliados';
        }

        const response = await axios.get(url, {
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
    <div className="ppcs-ja-avaliados-container">
      <h1>PPCs Avaliados</h1>
      <nav>
        <Link to="/dashboard" className="ppcs-ja-avaliados-back-link">Voltar</Link>
      </nav>
      {error && <p className="ppcs-ja-avaliados-error">{error}</p>}
      <div className="ppcs-ja-avaliados-list">
        {ppcs.map((ppc) => (
          <div key={ppc.id} className="ppcs-ja-avaliados-item">
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

export default PPCsJaAvaliados;
