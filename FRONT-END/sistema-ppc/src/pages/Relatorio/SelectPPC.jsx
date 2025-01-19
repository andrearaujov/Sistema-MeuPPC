// frontend/src/pages/Relatorio/SelectPPC.jsx

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';
import './SelectPPC.css';

const SelectPPC = () => {
  const [ppcs, setPPCs] = useState([]);
  const [error, setError] = useState('');
  const [selectedPPC, setSelectedPPC] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchPPCs = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('/api/ppcs', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        setPPCs(response.data);
      } catch (error) {
        setError('Erro ao carregar PPCs');
      }
    };

    fetchPPCs();
  }, []);

  const handleSelect = (event) => {
    setSelectedPPC(event.target.value);
  };

  const handleNavigate = (type) => {
    if (selectedPPC) {
      navigate(`/ppcs/${selectedPPC}/relatorio_${type}`);
    }
  };

  return (
    <div className="select-ppc-container">
      <h1>Selecione um PPC</h1>
      <nav>
        <Link to="/dashboard">Voltar</Link>
      </nav>
      {error && <p className="error">{error}</p>}
      <div className="select-ppc">
        <select value={selectedPPC} onChange={handleSelect}>
          <option value="">Escolha um PPC</option>
          {ppcs.map((ppc) => (
            <option key={ppc.id} value={ppc.id}>
              {ppc.titulo}
            </option>
          ))}
        </select>
        <button onClick={() => handleNavigate('colaboradores')}>Relatório de Colaboradores</button>
        <button onClick={() => handleNavigate('avaliadores')}>Relatório de Avaliadores</button>
        <button onClick={() => handleNavigate('participantes')}>Relatório de Participantes</button>
      </div>
    </div>
  );
};

export default SelectPPC;
