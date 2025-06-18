import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Tabs,
  Tab,
  TextField,
  Button,
  CircularProgress,
  Alert,
  Container,
} from '@mui/material';
import { useAuth } from '../hooks/useAuth.ts';
import { authApi } from '../lib/api/auth.ts';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div role="tabpanel" hidden={value !== index} {...other}>
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const ProfilePage: React.FC = () => {
  const { user, updateUser } = useAuth();
  const [tabIndex, setTabIndex] = useState(0);

  // States for profile update
  const [fullName, setFullName] = useState(user?.full_name || '');
  const [isProfileSaving, setProfileSaving] = useState(false);
  const [profileSuccess, setProfileSuccess] = useState('');
  const [profileError, setProfileError] = useState('');

  // States for password change
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isPasswordSaving, setPasswordSaving] = useState(false);
  const [passwordSuccess, setPasswordSuccess] = useState('');
  const [passwordError, setPasswordError] = useState('');

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabIndex(newValue);
  };

  const handleProfileSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setProfileSaving(true);
    setProfileError('');
    setProfileSuccess('');
    try {
      const updatedUser = await authApi.updateProfile({ full_name: fullName });
      updateUser(updatedUser);
      setProfileSuccess('Nome atualizado com sucesso!');
    } catch (err) {
      setProfileError('Falha ao atualizar o nome. Tente novamente.');
    } finally {
      setProfileSaving(false);
    }
  };

  const handlePasswordSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (newPassword !== confirmPassword) {
      setPasswordError('A nova senha e a confirmação não coincidem.');
      return;
    }
    setPasswordSaving(true);
    setPasswordError('');
    setPasswordSuccess('');
    try {
      await authApi.changePassword({ current_password: oldPassword, new_password: newPassword });
      setPasswordSuccess('Senha alterada com sucesso!');
      setOldPassword('');
      setNewPassword('');
      setConfirmPassword('');
    } catch (err: any) {
      setPasswordError(err.response?.data?.detail || 'Falha ao alterar a senha. Verifique sua senha atual.');
    } finally {
      setPasswordSaving(false);
    }
  };

  return (
    <Container maxWidth="md">
      <Typography variant="h4" gutterBottom sx={{ mb: 4, fontWeight: 'bold' }}>
        Meu Perfil
      </Typography>
      <Paper elevation={2}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={tabIndex} onChange={handleTabChange} aria-label="abas do perfil">
            <Tab label="Editar Perfil" />
            <Tab label="Alterar Senha" />
          </Tabs>
        </Box>
        <TabPanel value={tabIndex} index={0}>
          <Box component="form" onSubmit={handleProfileSubmit}>
            <Typography variant="h6" sx={{ mb: 2 }}>Informações do Usuário</Typography>
            {profileSuccess && <Alert severity="success" sx={{ mb: 2 }}>{profileSuccess}</Alert>}
            {profileError && <Alert severity="error" sx={{ mb: 2 }}>{profileError}</Alert>}
            <TextField
              label="Nome Completo"
              fullWidth
              margin="normal"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              disabled={isProfileSaving}
            />
            <Button type="submit" variant="contained" disabled={isProfileSaving} sx={{ mt: 2 }}>
              {isProfileSaving ? <CircularProgress size={24} /> : 'Salvar Alterações'}
            </Button>
          </Box>
        </TabPanel>
        <TabPanel value={tabIndex} index={1}>
          <Box component="form" onSubmit={handlePasswordSubmit}>
            <Typography variant="h6" sx={{ mb: 2 }}>Alteração de Senha</Typography>
            {passwordSuccess && <Alert severity="success" sx={{ mb: 2 }}>{passwordSuccess}</Alert>}
            {passwordError && <Alert severity="error" sx={{ mb: 2 }}>{passwordError}</Alert>}
            <TextField
              label="Senha Atual"
              type="password"
              fullWidth
              margin="normal"
              value={oldPassword}
              onChange={(e) => setOldPassword(e.target.value)}
              disabled={isPasswordSaving}
            />
            <TextField
              label="Nova Senha"
              type="password"
              fullWidth
              margin="normal"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              disabled={isPasswordSaving}
            />
            <TextField
              label="Confirmar Nova Senha"
              type="password"
              fullWidth
              margin="normal"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              disabled={isPasswordSaving}
            />
            <Button type="submit" variant="contained" disabled={isPasswordSaving} sx={{ mt: 2 }}>
              {isPasswordSaving ? <CircularProgress size={24} /> : 'Alterar Senha'}
            </Button>
          </Box>
        </TabPanel>
      </Paper>
    </Container>
  );
};

export default ProfilePage; 