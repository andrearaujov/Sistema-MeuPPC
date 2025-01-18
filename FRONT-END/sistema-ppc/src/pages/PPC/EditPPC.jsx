import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, Link, useNavigate } from 'react-router-dom';  // Alteração: Importando useNavigate
import {jwtDecode} from 'jwt-decode';
import './EditPPC.css';

const EditPPC = () => {
  const { id } = useParams();
  const navigate = useNavigate();  // Alteração: Criando uma instância de useNavigate
  const [ppc, setPPC] = useState(null);
  const [error, setError] = useState('');
  const [role, setRole] = useState('');
  const [newCollaboratorEmail, setNewCollaboratorEmail] = useState(''); // Novo estado para email do colaborador
  const [avaliadoresIds, setAvaliadoresIds] = useState(''); // Novo estado para IDs dos avaliadores

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
      console.log('Dados a serem salvos:', ppc);  // Log dos dados a serem salvos
      const response = await axios.put(`/api/ppcs/${id}`, ppc, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      console.log('Resposta do servidor:', response.data);  // Log da resposta do servidor
      alert('PPC salvo com sucesso!');
      navigate('/dashboard');  // Alteração: Redirecionando para o dashboard após salvar
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
    } catch (error) {
      console.error('Erro ao enviar para avaliação:', error);
      setError('Erro ao enviar para avaliação');
    }
  };

  return (
    <div>
      <h1>Editar PPC</h1>
      <nav>
        <Link to="/ppcs">Voltar</Link>
      </nav>
      {error && <p className="error">{error}</p>}
      {ppc && (
        <div className="ppc-edit-form">
          <label>
            Título:
            <input
              type="text"
              value={ppc.titulo}
              onChange={(e) => setPPC({ ...ppc, titulo: e.target.value })}
            />
          </label>
          <label>
            Descrição:
            <textarea
              value={ppc.descricao}
              onChange={(e) => setPPC({ ...ppc, descricao: e.target.value })}
            />
          </label>
          <button onClick={handleSave}>Salvar</button>
          {role === 'Coordenador' && (
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
