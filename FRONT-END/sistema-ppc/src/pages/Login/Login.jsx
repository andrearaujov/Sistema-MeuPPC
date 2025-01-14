// frontend/src/pages/Login/Login.jsx

import React, { useState } from "react";
import { FaUser, FaLock } from "react-icons/fa";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import "./Login.css";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [errorMessage, setErrorMessage] = useState("");

  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post("/api/users/login", { email, password });
      console.log("Login bem-sucedido:", response.data);

      // Armazena o token no localStorage
      localStorage.setItem("token", response.data.token);

      // Redireciona para a página principal ou dashboard
      navigate("/dashboard");
    } catch (error) {
      console.error("Erro ao fazer login:", error);
      setErrorMessage(error.response?.data?.error || "Erro ao fazer login.");
    }
  };

  return (
    <div className="login-container">
      <form onSubmit={handleSubmit}>
        <h1>Acesse o sistema</h1>
        {errorMessage && <p className="error">{errorMessage}</p>}
        <div className="input-field">
          <input
            type="email"
            placeholder="E-mail"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <FaUser className="icon" />
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

        <div className="recall-forget">
          <label>
            <input type="checkbox" />
            Lembre de mim
          </label>
          <a href="#">Esqueceu sua senha?</a>
        </div>
        <button type="submit">Login</button>
        <div className="signup-link">
          <p>
            Não tem uma conta? <Link to="/register">Registrar</Link>
          </p>
        </div>
      </form>
    </div>
  );
};

export default Login;
