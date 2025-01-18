import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';
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

  const filteredPPCs = ppcs.filter(ppc => {
    console.log('Colaboradores:', ppc.colaboradores);
    console.log('Role dentro do filtro:', role);
    console.log('User ID dentro do filtro:', userId);
    if (ppc.status !== 'Em Criacao') return false;
    if (role === 'Coordenador') return true;
    if (role === 'Colaborador') {
      const incluiColaborador = ppc.colaboradores.includes(String(userId));
      console.log(`Inclui colaborador ${userId}:`, incluiColaborador);
      return incluiColaborador;
    }
    if (role === 'Avaliador') {
      const incluiAvaliador = ppc.avaliadores.includes(String(userId)) && ppc.status === 'Em Avaliacao';
      console.log(`Inclui avaliador ${userId}:`, incluiAvaliador);
      return incluiAvaliador;
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
        <Link to="/dashboard">Home</Link>
      </nav>
      {error && <p className="error">{error}</p>}
      <div className="ppc-list">
        {filteredPPCs.length > 0 ? (
          filteredPPCs.map((ppc) => (
            <div key={ppc.id} className="ppc-item">
              <h2>{ppc.titulo}</h2>
              <p>{ppc.descricao}</p>
              {(role === 'Coordenador' || 
                (role === 'Colaborador' && ppc.colaboradores.includes(String(userId))) || 
                (role === 'Avaliador' && ppc.status === 'Em Avaliacao')) && (
                <Link to={`/ppcs/${ppc.id}`}>{role === 'Avaliador' ? 'Avaliar' : 'Editar'}</Link>
              )}
            </div>
          ))
        ) : (
          <p>Nenhum PPC encontrado.</p>
        )}
      </div>
      {role === 'Coordenador' && (
        <Link to="/ppcs/create" className="create-link">Criar Novo PPC</Link>
      )}
    </div>
  );
};

export default PPCs;
