import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, Link, useNavigate } from 'react-router-dom';
import {jwtDecode} from 'jwt-decode'; // Correta importação
import './EditPPC.css';

const EditPPC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [ppc, setPPC] = useState(null);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [saveSuccess, setSaveSuccess] = useState('');
  const [role, setRole] = useState('');
  const [newCollaboratorEmail, setNewCollaboratorEmail] = useState('');
  const [avaliadoresEmails, setAvaliadoresEmails] = useState('');

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

  useEffect(() => {
    if (success || saveSuccess) {
      const timer = setTimeout(() => {
        setSuccess('');
        setSaveSuccess('');
        // Redirecionar após limpar a mensagem de sucesso
        if (ppc && ppc.status !== 'Em Criacao') {
          navigate('/dashboard');
        }
      }, 3000); // Aguarda 3 segundos antes de limpar a mensagem e redirecionar
      return () => clearTimeout(timer);
    }
  }, [success, saveSuccess, navigate, ppc]);

  const handleSave = async () => {
    try {
      const token = localStorage.getItem('token');
      await axios.put(`/api/ppcs/${id}`, ppc, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      setSaveSuccess('PPC salvo com sucesso!');
      navigate('/ppcs');
    } catch (error) {
      setError('Erro ao salvar PPC');
    }
  };

  const handleAddCollaborator = async () => {
    try {
      const token = localStorage.getItem('token');
      await axios.post(`/api/ppcs/${id}/colaboradores`, { email: newCollaboratorEmail }, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      setSuccess('Colaborador adicionado com sucesso!');
      setNewCollaboratorEmail('');
    } catch (error) {
      setError('Erro ao adicionar colaborador');
    }
  };

  const handleSendForReview = async () => {
    try {
      const token = localStorage.getItem('token');
      await axios.post(`/api/ppcs/${id}/enviar_para_avaliacao`, { avaliadores_emails: avaliadoresEmails.split(',') }, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      setSuccess('PPC enviado para avaliação com sucesso!');
      setAvaliadoresEmails('');
    } catch (error) {
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
      {success && <p className="success-message">{success}</p>}
      {saveSuccess && <p className="success-message">{saveSuccess}</p>}
      {ppc && (
        <div className="edit-ppc-form">
          <label>
            Título:
            <input
              type="text"
              placeholder="Título"
              value={ppc.titulo}
              onChange={(e) => setPPC({ ...ppc, titulo: e.target.value })}
              disabled={!isEditable}
            />
          </label>
          <label>
            Descrição:
            <textarea
              placeholder="Descrição"
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
                    value={avaliadoresEmails}
                    onChange={(e) => setAvaliadoresEmails(e.target.value)}
                    placeholder="E-mails dos avaliadores, separados por vírgula"
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
