import React, { useState } from "react";
import axios from "axios";

const LoginForm = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://localhost:5000/login", {
        user: username,
        password: password,
      });
      console.log(res.data); // Aquí obtienes el token
    } catch (err) {
      if (err.response) {
        // Errores HTTP que devuelve el servidor
        setError(err.response.data.error);
      } else if (err.request) {
        // Errores que ocurren al realizar la solicitud
        setError("Error al realizar la solicitud");
      } else {
        // Otros errores
        setError("Error al iniciar sesión");
      }
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h3>Login</h3>
      {error && <div style={{ color: "red" }}>{error}</div>}
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button type="submit">Login</button>
    </form>
  );
};

export default LoginForm;
