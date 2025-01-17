import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';
import './EditPPC.css';

const EditPPC = () => {
  const { id } = useParams();
  const [titulo, setTitulo] = useState('');
  const [descricao, setDescricao] = useState('');
  const [colaboradorEmail, setColaboradorEmail] = useState('');
  const [avaliadoresIds, setAvaliadoresIds] = useState('');
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
      const token = localStorage.getItem('token');  // Supondo que o token está armazenado no localStorage
      await axios.put(`/api/ppcs/${id}`, { titulo, descricao }, { 
        headers: { 'Authorization': `Bearer ${token}` } 
      });
      navigate('/ppcs');
    } catch (error) {
      setError('Erro ao atualizar PPC');
    }
  };

  const handleAddColaborador = async (event) => {
    event.preventDefault();
    try {
      const token = localStorage.getItem('token');  // Supondo que o token está armazenado no localStorage
      await axios.post(`/api/ppcs/${id}/colaboradores`, 
        { email: colaboradorEmail }, 
        { headers: { 'Authorization': `Bearer ${token}` } }
      );
      setColaboradorEmail('');  // Limpa o campo de email
      setError('');  // Limpa os erros se o colaborador for adicionado com sucesso
    } catch (error) {
      setError('Erro ao adicionar colaborador');
    }
  };

  const handleSendForEvaluation = async (event) => {
    event.preventDefault();
    try {
      const token = localStorage.getItem('token');  // Supondo que o token está armazenado no localStorage
      const avaliadoresArray = avaliadoresIds.split(',').map(id => id.trim());
      await axios.post(`/api/ppcs/${id}/enviar_para_avaliacao`, 
        { avaliadores_ids: avaliadoresArray }, 
        { headers: { 'Authorization': `Bearer ${token}` } }
      );
      navigate('/ppcs');
    } catch (error) {
      setError('Erro ao enviar para avaliação');
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
      <h2>Adicionar Colaborador</h2>
      <form onSubmit={handleAddColaborador}>
        <div className="input-field">
          <input
            type="email"
            placeholder="Email do Colaborador"
            required
            value={colaboradorEmail}
            onChange={(e) => setColaboradorEmail(e.target.value)}
          />
        </div>
        <button type="submit">Adicionar Colaborador</button>
      </form>
      <h2>Enviar para Avaliação</h2>
      <form onSubmit={handleSendForEvaluation}>
        <div className="input-field">
          <input
            type="text"
            placeholder="IDs dos Avaliadores (separados por vírgula)"
            required
            value={avaliadoresIds}
            onChange={(e) => setAvaliadoresIds(e.target.value)}
          />
        </div>
        <button type="submit">Enviar para Avaliação</button>
      </form>
    </div>
  );
};

export default EditPPC;
