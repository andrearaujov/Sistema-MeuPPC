import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {jwtDecode} from 'jwt-decode';
import { Link } from 'react-router-dom';
import './PPCs.css';

const PPCs = () => {
  const [ppcs, setPPCs] = useState([]);
  const [error, setError] = useState('');
  const [role, setRole] = useState('');
  const [userId, setUserId] = useState('');

  useEffect(() => {
    const fetchPPCs = async () => {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          setError('Token não encontrado. Faça login novamente.');
          return;
        }

        const decodedToken = jwtDecode(token);
        setRole(decodedToken.papel);
        setUserId(decodedToken.id);

        let url = '/api/ppcs';
        if (decodedToken.papel === 'Colaborador') {
          url = '/api/colaboradores/ppcs';
        }

        const response = await axios.get(url, {
          headers: { 'Authorization': `Bearer ${token}` }
        });

        console.log('Response data:', response.data);
        setPPCs(response.data);
      } catch (error) {
        setError('Erro ao carregar PPCs');
        console.error('Erro ao carregar PPCs:', error);
      }
    };

    fetchPPCs();
  }, []);

  useEffect(() => {
    console.log('PPCs carregados:', ppcs);
  }, [ppcs]);

  useEffect(() => {
    console.log('Role:', role);
    console.log('User ID:', userId);
  }, [role, userId]);

  const handleDelete = async (ppcId) => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        alert('Token não encontrado. Faça login novamente.');
        return;
      }
  
      const response = await axios.post('/api/ppcs/delete', { ppc_id: ppcId }, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
  
      if (response.status === 200) {
        alert('PPC excluído com sucesso!');
        setPPCs(ppcs.filter(ppc => ppc.id !== ppcId));
      } else {
        alert(`Erro ao excluir PPC: ${response.data.error}`);
      }
    } catch (error) {
      alert('Erro ao excluir PPC');
      console.error('Erro ao excluir PPC:', error);
    }
  };
  
  

  const filteredPPCs = ppcs.filter(ppc => {
    if (ppc.status !== 'Em Criacao') return false;
    if (role === 'Coordenador') return true;
    if (role === 'Colaborador') {
      return ppc.colaboradores.includes(String(userId));
    }
    if (role === 'Avaliador') {
      return ppc.avaliadores.includes(String(userId)) && ppc.status === 'Em Avaliacao';
    }
    return false;
  });

  useEffect(() => {
    console.log('Filtered PPCs:', filteredPPCs);
  }, [filteredPPCs]);

  return (
    <div>
      <h1>Gerenciamento de PPCs</h1>
      <nav>
        <Link to="/dashboard" className="ppcs-home-link">Home</Link>
      </nav>
      {error && <p className="ppcs-error">{error}</p>}
      <div className="ppcs-ppc-list">
        {filteredPPCs.length > 0 ? (
          filteredPPCs.map((ppc) => (
            <div key={ppc.id} className="ppcs-ppc-item">
              <h2>{ppc.titulo}</h2>
              <p>{ppc.descricao}</p>
              {(role === 'Coordenador' || 
                (role === 'Colaborador' && ppc.colaboradores.includes(String(userId))) || 
                (role === 'Avaliador' && ppc.status === 'Em Avaliacao')) && (
                <Link to={`/ppcs/${ppc.id}`}>{role === 'Avaliador' ? 'Avaliar' : 'Editar'}</Link>
              )}
              {role === 'Coordenador' && ppc.status === 'Em Criacao' && (
                <button onClick={() => handleDelete(ppc.id)} className="delete-btn">Excluir</button>
              )}
            </div>
          ))
        ) : (
          <p>Nenhum PPC encontrado.</p>
        )}
      </div>
      {role === 'Coordenador' && (
        <Link to="/ppcs/create" className="ppcs-create-link">Criar Novo PPC</Link>
      )}
    </div>
  );
};

export default PPCs;
