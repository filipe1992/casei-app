import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Container,
  Paper,
  Alert,
  CircularProgress,
  Button,
} from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import { authApi } from '../lib/api/auth.ts';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';

const ConfirmEmail = () => {
  const { token } = useParams<{ token: string }>();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    const verifyEmail = async () => {
      if (!token) {
        setError('Token de confirmação não fornecido.');
        setLoading(false);
        return;
      }

      try {
        const response = await authApi.confirmEmail(token);
        setSuccess(response.message);
      } catch (err: any) {
        const errorMessage = err.response?.data?.detail || 'Ocorreu um erro ao confirmar seu e-mail.';
        setError(errorMessage);
      } finally {
        setLoading(false);
      }
    };

    verifyEmail();
  }, [token]);

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: 'grey.100',
      }}
    >
      <Container component="main" maxWidth="sm">
        <Paper elevation={3} sx={{ p: 4, display: 'flex', flexDirection: 'column', alignItems: 'center', borderRadius: 2 }}>
          <Typography component="h1" variant="h5" sx={{ mb: 3, fontWeight: 600 }}>
            Confirmação de E-mail
          </Typography>

          {loading && (
            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2 }}>
              <CircularProgress />
              <Typography>Verificando seu e-mail...</Typography>
            </Box>
          )}

          {error && (
            <Alert severity="error" icon={<ErrorOutlineIcon />} sx={{ width: '100%', alignItems: 'center' }}>
              {error}
            </Alert>
          )}
          
          {success && (
            <Alert severity="success" icon={<CheckCircleOutlineIcon />} sx={{ width: '100%', alignItems: 'center' }}>
              {success}
            </Alert>
          )}

          <Button
            variant="contained"
            onClick={() => navigate('/login')}
            sx={{ mt: 3 }}
          >
            Ir para o Login
          </Button>
        </Paper>
      </Container>
    </Box>
  );
};

export default ConfirmEmail; 