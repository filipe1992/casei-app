import React, { useState, useEffect } from 'react';
import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  TextField,
  CircularProgress
} from '@mui/material';
import { Guest } from '../../types/guest.ts';
import { GuestUpdatePayload } from '../../lib/api/guest.ts';

interface EditGuestDialogProps {
  open: boolean;
  onClose: () => void;
  guest: Guest | null;
  onEditGuest: (guestId: number, payload: GuestUpdatePayload) => Promise<void>;
}

const EditGuestDialog: React.FC<EditGuestDialogProps> = ({ open, onClose, guest, onEditGuest }) => {
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    if (guest) {
      setName(guest.name);
      setPhone(guest.phone);
    }
  }, [guest]);

  const handleSubmit = async () => {
    if (guest && name && phone) {
      setIsSaving(true);
      try {
        await onEditGuest(guest.id, { name, phone });
        onClose();
      } catch (error) {
        console.error("Failed to edit guest:", error);
      } finally {
        setIsSaving(false);
      }
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Editar Convidado</DialogTitle>
      <DialogContent>
        <TextField
          autoFocus
          margin="dense"
          label="Nome Completo"
          type="text"
          fullWidth
          variant="outlined"
          value={name}
          onChange={(e) => setName(e.target.value)}
          disabled={isSaving}
        />
        <TextField
          margin="dense"
          label="Telefone (com DDD)"
          type="tel"
          fullWidth
          variant="outlined"
          value={phone}
          onChange={(e) => setPhone(e.target.value)}
          disabled={isSaving}
        />
      </DialogContent>
      <DialogActions sx={{ p: 3 }}>
        <Button onClick={onClose} color="secondary" disabled={isSaving}>
          Cancelar
        </Button>
        <Button onClick={handleSubmit} variant="contained" disabled={!name || !phone || isSaving}>
          {isSaving ? <CircularProgress size={24} color="inherit" /> : 'Salvar'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default EditGuestDialog; 