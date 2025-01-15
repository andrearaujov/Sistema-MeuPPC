import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';
import './EditPPC.css';

const EditPPC = () => {
  const { id } = useParams();
  const [titulo, setTitulo] = useState('');
  const [descricao, setDescricao] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchPPC = async () => {
      try {
        const response = await axios.get(`/api/ppcs/${id}`);
        setTitulo(response.data.titulo);
        setDescricao(response.data.descricao);
      } catch (error) {
        setError('Erro ao carregar PPC');
      }
    };

    fetchPPC();
  }, [id]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      await axios.put(`/api/ppcs/${id}`, { titulo, descricao });
      navigate('/ppcs');
    } catch (error) {
      setError('Erro ao atualizar PPC');
    }
  };

  return (
    <div>
      <h1>Editar PPC</h1>
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
        <button type="submit">Atualizar</button>
      </form>
    </div>
  );
};

export default EditPPC;
