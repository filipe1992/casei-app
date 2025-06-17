import React, { useState } from 'react';
import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  TextField,
  CircularProgress
} from '@mui/material';

interface AddGuestDialogProps {
  open: boolean;
  onClose: () => void;
  onAddGuest: (name: string, phone: string) => Promise<void>;
}

const AddGuestDialog: React.FC<AddGuestDialogProps> = ({ open, onClose, onAddGuest }) => {
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [isAdding, setIsAdding] = useState(false);

  const handleSubmit = async () => {
    if (name && phone) {
      setIsAdding(true);
      try {
        await onAddGuest(name, phone);
        handleClose();
      } catch (error) {
        console.error("Failed to add guest:", error);
        // Here you could show an error message to the user
      } finally {
        setIsAdding(false);
      }
    }
  };

  const handleClose = () => {
    setName('');
    setPhone('');
    onClose();
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
      <DialogTitle>Adicionar Novo Convidado</DialogTitle>
      <DialogContent>
        <TextField
          autoFocus
          margin="dense"
          id="name"
          label="Nome Completo"
          type="text"
          fullWidth
          variant="outlined"
          value={name}
          onChange={(e) => setName(e.target.value)}
          disabled={isAdding}
        />
        <TextField
          margin="dense"
          id="phone"
          label="Telefone (com DDD)"
          type="tel"
          fullWidth
          variant="outlined"
          value={phone}
          onChange={(e) => setPhone(e.target.value)}
          disabled={isAdding}
        />
      </DialogContent>
      <DialogActions sx={{ p: 3 }}>
        <Button onClick={handleClose} color="secondary" disabled={isAdding}>
          Cancelar
        </Button>
        <Button onClick={handleSubmit} variant="contained" disabled={!name || !phone || isAdding}>
          {isAdding ? <CircularProgress size={24} color="inherit" /> : 'Adicionar'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default AddGuestDialog; 