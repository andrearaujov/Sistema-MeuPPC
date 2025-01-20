import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';
import './PPCsNaoAvaliados.css';

const PPCsNaoAvaliados = () => {
  const [ppcs, setPPCs] = useState([]);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [rejectionReasons, setRejectionReasons] = useState({});

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

  const handleApprove = async (ppcId) => {
    try {
      const token = localStorage.getItem('token');
      await axios.post(`/api/avaliadores/ppcs/${ppcId}/aprovar`, {}, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      setSuccess(`PPC ${ppcId} aprovado com sucesso!`);
      setPPCs(ppcs.filter(ppc => ppc.id !== ppcId)); // Remover o PPC aprovado da lista
    } catch (error) {
      setError('Erro ao aprovar PPC');
    }
  };

  const handleReject = async (ppcId) => {
    try {
      const token = localStorage.getItem('token');
      await axios.post(`/api/avaliadores/ppcs/${ppcId}/rejeitar`, { descricao: rejectionReasons[ppcId] }, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      setSuccess(`PPC ${ppcId} rejeitado com sucesso!`);
      setPPCs(ppcs.filter(ppc => ppc.id !== ppcId)); // Remover o PPC rejeitado da lista
    } catch (error) {
      setError('Erro ao rejeitar PPC');
    }
  };

  const handleRejectionReasonChange = (ppcId, value) => {
    setRejectionReasons(prev => ({ ...prev, [ppcId]: value }));
  };

  return (
    <div className="ppcs-nao-avaliados-container">
      <h1>PPCs Não Avaliados</h1>
      <nav>
        <Link to="/dashboard" className="ppcs-nao-avaliados-back-link">Voltar</Link>
      </nav>
      {error && <p className="ppcs-nao-avaliados-error">{error}</p>}
      {success && <p className="ppcs-nao-avaliados-success">{success}</p>}
      <div className="ppcs-nao-avaliados-list">
        {ppcs.map((ppc) => (
          <div key={ppc.id} className="ppcs-nao-avaliados-item">
            <h3>{ppc.titulo}</h3>
            <p>{ppc.descricao}</p>
            <Link to={`/avaliar/${ppc.id}`} className="ppcs-nao-avaliados-edit-link">
              Avaliar
            </Link>
            <button onClick={() => handleApprove(ppc.id)} className="ppcs-nao-avaliados-approve-btn">Aprovar</button>
            <textarea
              placeholder="Descreva a razão da rejeição"
              value={rejectionReasons[ppc.id] || ''}
              onChange={(e) => handleRejectionReasonChange(ppc.id, e.target.value)}
              className="ppcs-nao-avaliados-rejection-reason"
            ></textarea>
            <button onClick={() => handleReject(ppc.id)} className="ppcs-nao-avaliados-reject-btn">Rejeitar</button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PPCsNaoAvaliados;
