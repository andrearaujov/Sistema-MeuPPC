// frontend/src/pages/Register/Register.jsx

import React, { useState } from 'react';
import { FaUser, FaEnvelope, FaLock } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Register.css'; 

const Register = () => {
  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (password !== confirmPassword) {
      setErrorMessage('As senhas não coincidem.');
      return;
    }

    try {
      const response = await axios.post('/api/users/register', { nome, email, password });
      console.log('Usuário registrado com sucesso:', response.data);
      setSuccessMessage('Registro realizado com sucesso!');

      // Redireciona para a página de login
      navigate('/');
    } catch (error) {
      console.error('Erro ao registrar usuário:', error);
      setErrorMessage(error.response?.data?.error || 'Erro ao registrar usuário.');
    }
  };

  return (
    <div className="container">
      <form onSubmit={handleSubmit}>
        <h1>Registre-se</h1>
        {errorMessage && <p className="error">{errorMessage}</p>}
        {successMessage && <p className="success">{successMessage}</p>}
        <div className="input-field">
          <input
            type="text"
            placeholder="Nome"
            required
            value={nome}
            onChange={(e) => setNome(e.target.value)}
          />
          <FaUser className="icon" />
        </div>
        <div className="input-field">
          <input
            type="email"
            placeholder="E-mail"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <FaEnvelope className="icon" />
        </div>
        <div className="input-field">
          <input
            type="password"
            placeholder="Senha"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <FaLock className="icon" />
        </div>
        <div className="input-field">
          <input
            type="password"
            placeholder="Confirme a Senha"
            required
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
          <FaLock className="icon" />
        </div>

        <button type="submit">Registrar</button>
      </form>
    </div>
  );
};

export default Register;
