import React, { useState } from "react";
import { Container, Typography, Card, TextField, Button, Box, Link, InputAdornment } from "@mui/material";
import { Lock, Email } from "@mui/icons-material";
import Footer from "../components/Footer";

const LoginPage = ({ onLogin }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = () => {
    if (email && password) {
      onLogin(); // Aqui você pode conectar ao sistema de autenticação real
    } else {
      alert("Por favor, preencha ambos os campos!");
    }
  };

  const handleForgotPassword = () => {
    alert(`Um link de recuperação foi enviado para: ${email}`);
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center", height: "100vh", width: "100%" }}>
    <div style={{ position: "absolute", top: 0, left: 0, right: 0, bottom: 0, display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center", height: "100", width: "100%", backgroundColor: "#f5f5f5" }}>
    <Container maxWidth="lg" sx={{ mt: 8, display: "flex", flexDirection: "row", justifyContent: "center", alignItems: "center", height: "100vh", width: "100%" }}>
      <Card sx={{ p: 4, textAlign: "center", boxShadow: 3 }}>
        <Lock sx={{ fontSize: 48, color: "#d1d5db", mb: 2 }} />
        <Typography variant="h5" sx={{ fontWeight: "bold", color: "#111827", mb: 2 }}>
          Acessar o Painel
        </Typography>
        <Typography variant="body2" sx={{ color: "#6b7280", mb: 4 }}>
          Digite seu e-mail e senha para acessar sua conta.
        </Typography>

        <TextField
          type="email"
          variant="outlined"
          fullWidth
          placeholder="Digite seu e-mail"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          sx={{ mb: 2 }}
          slotProps={{
            input: {
              startAdornment: (
                <InputAdornment position="start">
                  <Email />
                </InputAdornment>
              ),
            },
          }}
        />

        <TextField
          type="password"
          variant="outlined"
          fullWidth
          placeholder="Digite sua senha"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          sx={{ mb: 2 }}
        />

        <Button variant="contained" color="primary" fullWidth onClick={handleLogin}>
          Entrar
        </Button>

        <Box sx={{ mt: 2 }}>
          <Link
            href="#"
            onClick={handleForgotPassword}
            sx={{ color: "#db2777", fontSize: 14, cursor: "pointer" }}
          >
            Esqueci minha senha
          </Link>
        </Box>
      </Card>
    </Container>
    </div>
    <Footer />
    </div>
  );
};

export default LoginPage;
