import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { jwtDecode } from "jwt-decode";
import './CreatePPC.css';

const CreatePPC = () => {
  const [titulo, setTitulo] = useState('');
  const [descricao, setDescricao] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      // Recupera o token do localStorage
      const token = localStorage.getItem('token');

      // Decodifica o token para obter o coordenador_id
      const decodedToken = jwtDecode(token);
      const coordenador_id = decodedToken.id; // Obtém o coordenador_id do token decodificado

      // Faz a solicitação para criar o PPC com o cabeçalho de autorização
      await axios.post('/api/ppcs', { titulo, descricao, coordenador_id }, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      // Redireciona para a página de PPCs
      navigate('/ppcs');
    } catch (error) {
      setError('Erro ao criar PPC');
    }
  };

  return (
    <div>
      <h1>Criar Novo PPC</h1>
      {error && <p className="error">{error}</p>}
      <form onSubmit={handleSubmit}>
        <div className="input-field">
          <input
            type="text"
            placeholder="Título"
            required
            value={titulo}
            onChange={(e) => setTitulo(e.target.value)}
          />
        </div>
        <div className="input-field">
          <textarea
            placeholder="Descrição"
            required
            value={descricao}
            onChange={(e) => setDescricao(e.target.value)}
          ></textarea>
        </div>
        <button type="submit">Criar</button>
      </form>
    </div>
  );
};

export default CreatePPC;
