import React, { useState } from 'react';
import { FaUser, FaEnvelope, FaLock } from 'react-icons/fa';
import './Register.css'; 

const Register = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  // Função que é chamada quando o formulário é enviado
  const handleSubmit = (event) => {
    event.preventDefault();

    // Aqui você pode adicionar a lógica para registrar o usuário, enviando os dados para a API
    console.log('Dados do novo usuário:', { name, email, password });

    // Exemplo de lógica para enviar os dados do formulário a uma API (isso é apenas ilustrativo)
    // axios.post('URL_API', { name, email, password })
    //   .then(response => {
    //     console.log('Usuário registrado com sucesso:', response.data);
    //   })
    //   .catch(error => {
    //     console.error('Erro ao registrar usuário:', error);
    //   });
  };

  return (
    <div className="container">
      <form onSubmit={handleSubmit}>
        <h1>Registre-se</h1>
        <div className="input-field">
          <input
            type="text"
            placeholder="Nome"
            required
            value={name}
            onChange={(e) => setName(e.target.value)}
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

        <button type="submit">Registrar</button>
      </form>
    </div>
  );
};

export default Register;
