import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';
import './EditPPC.css';

const EditPPC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [ppc, setPPC] = useState(null);
  const [error, setError] = useState('');
  const [role, setRole] = useState('');
  const [newCollaboratorEmail, setNewCollaboratorEmail] = useState('');
  const [avaliadoresIds, setAvaliadoresIds] = useState('');

  useEffect(() => {
    const fetchPPC = async () => {
      try {
        const token = localStorage.getItem('token');
        const decodedToken = jwtDecode(token);
        setRole(decodedToken.papel);

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

  const handleSave = async () => {
    try {
      const token = localStorage.getItem('token');
      console.log('Dados a serem salvos:', ppc);
      const response = await axios.put(`/api/ppcs/${id}`, ppc, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      console.log('Resposta do servidor:', response.data);
      alert('PPC salvo com sucesso!');
      navigate('/dashboard');
    } catch (error) {
      console.error('Erro ao salvar PPC:', error);
      setError('Erro ao salvar PPC');
    }
  };

  const handleAddCollaborator = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(`/api/ppcs/${id}/colaboradores`, { email: newCollaboratorEmail }, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      alert('Colaborador adicionado com sucesso!');
      setNewCollaboratorEmail('');
    } catch (error) {
      console.error('Erro ao adicionar colaborador:', error);
      setError('Erro ao adicionar colaborador');
    }
  };

  const handleSendForReview = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(`/api/ppcs/${id}/enviar_para_avaliacao`, { avaliadores_ids: avaliadoresIds.split(',') }, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      alert('PPC enviado para avaliação com sucesso!');
      if (response.data.redirect_url) {
        navigate(response.data.redirect_url);  // Redirecionar para o dashboard após enviar para avaliação
      }
    } catch (error) {
      console.error('Erro ao enviar para avaliação:', error);
      setError('Erro ao enviar para avaliação');
    }
  };

  const isEditable = ppc && ppc.status === 'Em Criacao';

  return (
    <div className="edit-ppc-container">
      <h1>Editar PPC</h1>
      <nav>
        <Link to="/ppcs" className="edit-ppc-back-btn">Voltar</Link>
      </nav>
      {error && <p className="edit-ppc-error">{error}</p>}
      {ppc && (
        <div className="edit-ppc-form">
          <label>
            Título:
            <input
              type="text"
              value={ppc.titulo}
              onChange={(e) => setPPC({ ...ppc, titulo: e.target.value })}
              disabled={!isEditable}
            />
          </label>
          <label>
            Descrição:
            <textarea
              value={ppc.descricao}
              onChange={(e) => setPPC({ ...ppc, descricao: e.target.value })}
              disabled={!isEditable}
            />
          </label>
          <button onClick={handleSave} disabled={!isEditable}>Salvar</button>
          {role === 'Coordenador' && isEditable && (
            <div>
              <div>
                <label>
                  Adicionar Colaborador:
                  <input
                    type="email"
                    value={newCollaboratorEmail}
                    onChange={(e) => setNewCollaboratorEmail(e.target.value)}
                    placeholder="Email do colaborador"
                  />
                </label>
                <button onClick={handleAddCollaborator}>Adicionar Colaborador</button>
              </div>
              <div>
                <label>
                  Enviar para Avaliação:
                  <input
                    type="text"
                    value={avaliadoresIds}
                    onChange={(e) => setAvaliadoresIds(e.target.value)}
                    placeholder="IDs dos avaliadores, separados por vírgula"
                  />
                </label>
                <button onClick={handleSendForReview}>Enviar para Avaliação</button>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default EditPPC;
