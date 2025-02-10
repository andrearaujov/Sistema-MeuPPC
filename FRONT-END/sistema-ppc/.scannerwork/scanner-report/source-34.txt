import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { jwtDecode } from "jwt-decode";
import './CreatePPC.css';

const CreatePPC = () => {
  const [titulo, setTitulo] = useState('');
  const [descricao, setDescricao] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      const decodedToken = jwtDecode(token);
      if (decodedToken.papel !== 'Coordenador') {
        navigate('/dashboard'); // Redireciona se o usuário não for um coordenador
      }
    }
  }, [navigate]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const token = localStorage.getItem('token');
      await axios.post('/api/ppcs', { titulo, descricao }, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      navigate('/ppcs');
    } catch (error) {
      setError('Erro ao criar PPC');
    }
  };

  return (
    <div>
      <h1>Criar Novo PPC</h1>
      {error && <p className="create-ppc-error">{error}</p>}
      <form onSubmit={handleSubmit}>
        <div className="create-ppc-input-field">
          <input
            type="text"
            placeholder="Título"
            required
            value={titulo}
            onChange={(e) => setTitulo(e.target.value)}
          />
        </div>
        <div className="create-ppc-input-field">
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
