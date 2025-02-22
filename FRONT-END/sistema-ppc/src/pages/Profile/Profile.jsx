import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Profile.css';

const Profile = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const token = localStorage.getItem('token');
        console.log('Token:', token);

        if (!token) {
          console.log('Redirecionando para login');
          navigate('/login');
          return;
        }

        const response = await axios.get('http://localhost:5000/api/perfil', {
          headers: { 'Authorization': `Bearer ${token}` }
        });

        console.log('Resposta do servidor:', response.data);
        setUser(response.data);
      } catch (error) {
        setError('Erro ao carregar perfil');
        console.error('Erro ao carregar perfil:', error.message);
        console.error('Erro detalhes:', error.config);
        console.error('Erro resposta:', error.response);
        console.error('Erro solicitação:', error.request);
      }
    };

    fetchProfile();
  }, [navigate]);

  return (
    <div className="profile-container">
      <h1>Perfil do Usuário</h1>
      {error && <p className="error">{error}</p>}
      {user ? (
        <div className="profile-info">
          <p><strong>Nome:</strong> {user.nome}</p>
          <p><strong>Email:</strong> {user.email}</p>
        </div>
      ) : (
        <p>Carregando...</p>
      )}
      <button onClick={() => navigate('/dashboard')}>Voltar ao Dashboard</button>
    </div>
  );
};

export default Profile;
