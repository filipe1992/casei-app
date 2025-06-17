import React, { useState } from 'react';
import {
  Box,
  Button,
  TextField,
  Typography,
  Container,
  Paper,
  Grid,
  Alert,
  CircularProgress,
  Link,
} from '@mui/material';
import { useNavigate, Link as RouterLink } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth.ts';
import { RegisterData } from '../lib/api/auth.ts';

const Register: React.FC = () => {
  const navigate = useNavigate();
  const { register } = useAuth();
  const [error, setError] = useState('');
  const [emailError, setEmailError] = useState('');
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState<RegisterData>({
    email: '',
    full_name: '',
    password: '',
  });
  const [confirmPassword, setConfirmPassword] = useState('');
  const [passwordError, setPasswordError] = useState('');

  const handleChange = (field: keyof RegisterData) => (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setEmailError('');
    setFormData({
      ...formData,
      [field]: event.target.value,
    });

    if (field === 'email' && !event.target.value.includes('@')) {
      setEmailError('Por favor, insira um email válido.');
      return;
    }

  };

  const handleChangeConfirmPassword = (event: React.ChangeEvent<HTMLInputElement>) => {
    setConfirmPassword(event.target.value);
    setPasswordError('');

    if (event.target.value !== formData.password) {
      setPasswordError('As senhas não coincidem.');
    }
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError('');
    setLoading(true);

    try {
      await register(formData);
      navigate('/login');
    } catch (error) {
      console.error('Erro ao cadastrar:', error);
      setError(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundImage: 'url("/background.jpg")',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        py: 4,
        '&::before': {
          content: '""',
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(255, 255, 255, 0.3)',
          backdropFilter: 'blur(8px)',
        },
      }}
    >
      <Container component="main" maxWidth="sm" sx={{ position: 'relative', zIndex: 1 }}>
        <Paper
          elevation={3}
          sx={{
            p: 4,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            backgroundColor: 'rgba(255, 255, 255, 0.9)',
            borderRadius: 2,
            boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)',
          }}
        >
          <Box
            sx={{
              mb: 3,
              width: '150px',
              height: '150px',
              backgroundImage: 'url("/logo.svg")',
              backgroundSize: 'contain',
              backgroundRepeat: 'no-repeat',
              backgroundPosition: 'center',
              filter: 'drop-shadow(0 4px 8px rgba(0, 0, 0, 0.1))',
            }}
          />
          <Typography component="h1" variant="h5" sx={{ mb: 3, fontWeight: 600 }}>
            Cadastro
          </Typography>

          {error && (
            <Alert severity="error" sx={{ mb: 2, width: '100%' }}>
              {error}
            </Alert>
          )}

          <Box component="form" onSubmit={handleSubmit} sx={{ width: '100%' }}>
            <Grid container direction='column' spacing={5} sx={{alignItems:'stretch', justifyContent:'center'}}>
            <Grid>
                <TextField
                  required
                  fullWidth
                  label="Nome Completo"
                  type="text"
                  value={formData.full_name}
                  onChange={handleChange('full_name')}
                  disabled={loading}
                  autoFocus
                />
              </Grid>
              <Grid >
                <TextField
                  error={!!emailError}
                  helperText={emailError}
                  required
                  fullWidth
                  label="Email"
                  type="email"
                  value={formData.email}
                  onChange={handleChange('email')}
                  disabled={loading}
                />
              </Grid>
              <Grid>
                <TextField
                  error={!!passwordError}
                  helperText={passwordError}
                  required
                  fullWidth
                  label="Senha"
                  type="password"
                  value={formData.password}
                  onChange={handleChange('password')}
                  disabled={loading}
                />
              </Grid>
              <Grid>
                <TextField
                  error={!!passwordError}
                  helperText={passwordError}
                  required
                  fullWidth
                  label="Confirmação de senha "
                  type="password"
                  value={confirmPassword}
                  onChange={handleChangeConfirmPassword}
                  disabled={loading}
                />
              </Grid>
            </Grid>

            <Button
              type="submit"
              fullWidth
              variant="contained"
              disabled={loading}
              sx={{
                mt: 3,
                mb: 2,
                py: 1.5,
                backgroundColor: '#2196f3',
                '&:hover': {
                  backgroundColor: '#1976d2',
                },
              }}
            >
              {loading ? (
                <CircularProgress size={24} sx={{ color: 'white' }} />
              ) : (
                'Cadastrar'
              )}
            </Button>

            <Grid container justifyContent="center">
              <Grid>
                <Link
                  component={RouterLink}
                  to="/login"
                  variant="body2"
                  sx={{
                    color: '#666',
                    textDecoration: 'none',
                    '&:hover': {
                      textDecoration: 'underline',
                    },
                  }}
                >
                  Já tem uma conta? Faça login
                </Link>
              </Grid>
            </Grid>
          </Box>
        </Paper>
      </Container>
    </Box>
  );
};

export default Register;